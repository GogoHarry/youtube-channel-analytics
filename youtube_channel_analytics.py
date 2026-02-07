"""
===============================================================================
YOUTUBE CHANNEL CONTENT ANALYTICS PROJECT - COMPLETE VERSION
===============================================================================
Includes all three hypothesis tests:
1. Shorter videos have higher engagement
2. Videos published on specific days perform better
3. Tutorial videos get more views than career advice videos
===============================================================================
"""

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, f_oneway, ttest_ind, mannwhitneyu
from collections import Counter
from googleapiclient.discovery import build
from dotenv import load_dotenv
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

class YouTubeConfig:
    """Configuration class for YouTube API settings"""
    
    def __init__(self, env_path=None):
        """
        Initialize YouTube API configuration
        
        Args:
            env_path (str): Path to .env file containing API key
        """
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()
        
        self.api_key = os.getenv('API_KEY')
        self.channel_id = "UC7cs8q-gJRlGwj4A8OmCmXg"  # Alex The Analyst
        
        if not self.api_key:
            raise ValueError("API_KEY not found. Please set it in your .env file")
    
    def build_youtube_client(self):
        """Build and return YouTube API client"""
        return build('youtube', 'v3', developerKey=self.api_key)


# ============================================================================
# DATA EXTRACTION
# ============================================================================

class YouTubeDataExtractor:
    """Class to handle YouTube data extraction"""
    
    def __init__(self, youtube_client, channel_id):
        """
        Initialize the data extractor
        
        Args:
            youtube_client: YouTube API client
            channel_id (str): YouTube channel ID
        """
        self.youtube = youtube_client
        self.channel_id = channel_id
    
    def get_upload_playlist_id(self):
        """
        Get the playlist ID containing all uploaded videos
        
        Returns:
            str: Upload playlist ID
        """
        try:
            channel_info = self.youtube.channels().list(
                part='contentDetails',
                id=self.channel_id
            ).execute()
            
            return channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        except Exception as e:
            print(f"Error fetching upload playlist: {e}")
            return None
    
    def get_all_video_ids(self, playlist_id):
        """
        Fetch all video IDs from a playlist
        
        Args:
            playlist_id (str): Playlist ID to fetch videos from
            
        Returns:
            list: List of video IDs
        """
        video_ids = []
        next_page_token = None
        
        try:
            while True:
                response = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                page_videos = [
                    item['contentDetails']['videoId'] 
                    for item in response.get('items', [])
                ]
                video_ids.extend(page_videos)
                
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
            
            print(f"✓ Successfully fetched {len(video_ids)} video IDs")
            return video_ids
        
        except Exception as e:
            print(f"Error fetching video IDs: {e}")
            return []
    
    def get_video_details(self, video_ids):
        """
        Fetch detailed metadata for list of video IDs
        
        Args:
            video_ids (list): List of video IDs
            
        Returns:
            list: List of dictionaries containing video metadata
        """
        stats = []
        
        try:
            # Process in batches of 50 (API limit)
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i+50]
                
                request = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(batch)
                )
                response = request.execute()
                
                for item in response['items']:
                    data = {
                        'video_id': item['id'],
                        'title': item['snippet']['title'],
                        'views': int(item['statistics'].get('viewCount', 0)),
                        'likes': int(item['statistics'].get('likeCount', 0)),
                        'comments': int(item['statistics'].get('commentCount', 0)),
                        'duration': item['contentDetails']['duration'],
                        'published': item['snippet']['publishedAt'],
                        'description': item['snippet'].get('description', ''),
                        'tags': item['snippet'].get('tags', [])
                    }
                    stats.append(data)
            
            print(f"✓ Successfully fetched details for {len(stats)} videos")
            return stats
        
        except Exception as e:
            print(f"Error fetching video details: {e}")
            return []


# ============================================================================
# DATA PROCESSING
# ============================================================================

class YouTubeDataProcessor:
    """Class to process and transform YouTube data"""
    
    @staticmethod
    def duration_to_seconds(duration):
        """
        Convert ISO 8601 duration to seconds
        
        Args:
            duration (str): ISO 8601 duration string (e.g., 'PT15M30S')
            
        Returns:
            int: Duration in seconds
        """
        hours = re.search(r'(\d+)H', duration)
        minutes = re.search(r'(\d+)M', duration)
        seconds = re.search(r'(\d+)S', duration)
        
        total = 0
        if hours:
            total += int(hours.group(1)) * 3600
        if minutes:
            total += int(minutes.group(1)) * 60
        if seconds:
            total += int(seconds.group(1))
        
        return total
    
    @staticmethod
    def categorize_video_type(title):
        """
        Categorize video based on title keywords
        
        Args:
            title (str): Video title
            
        Returns:
            str: Video category
        """
        title_lower = title.lower()
        
        # Define category keywords with priority order (more specific first)
        categories = {
            'Tutorial': ['tutorial', 'how to', 'guide', 'learn', 'beginner', 
                        'advanced', 'intermediate', 'basics', 'step by step',
                        'complete', 'full course', 'training'],
            'Career': ['career', 'job', 'salary', 'interview', 'resume', 'hiring',
                      'work', 'employment', 'promotion', 'cv', 'recruiter'],
            'Project': ['project', 'portfolio', 'bootcamp', 'full project',
                       'hands-on', 'practical', 'real world'],
            'Tools': ['excel', 'sql', 'python', 'tableau', 'power bi', 'pandas',
                     'mysql', 'jupyter', 'anaconda', 'azure', 'aws'],
            'Q&A/Livestream': ['q&a', 'qa', 'livestream', 'ask me anything', 'ama',
                              'live', 'questions', 'answers'],
            'Advice': ['tips', 'mistakes', 'reasons', 'best', 'top', 'avoid',
                      'should', 'shouldn\'t', 'advice', 'recommendation']
        }
        
        # Check each category in order
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'Other'
    
    @staticmethod
    def process_dataframe(df):
        """
        Process raw dataframe and add derived columns
        
        Args:
            df (pd.DataFrame): Raw video data
            
        Returns:
            pd.DataFrame: Processed dataframe with additional metrics
        """
        # Convert duration to seconds and minutes
        df['duration_sec'] = df['duration'].apply(
            YouTubeDataProcessor.duration_to_seconds
        )
        df['duration_min'] = df['duration_sec'] / 60
        
        # Calculate engagement metrics (avoid division by zero)
        df['likes_per_view'] = df['likes'] / df['views'].replace(0, 1)
        df['comments_per_view'] = df['comments'] / df['views'].replace(0, 1)
        df['engagement_rate'] = (df['likes'] + df['comments']) / df['views'].replace(0, 1)
        
        # Convert published date to datetime
        df['published'] = pd.to_datetime(df['published'])
        
        # Extract temporal features
        df['upload_quarter'] = df['published'].dt.to_period('Q').astype(str)
        df['day_of_week'] = df['published'].dt.dayofweek
        df['day_name'] = df['published'].dt.day_name()
        df['month'] = df['published'].dt.month
        df['year'] = df['published'].dt.year
        
        # Categorize videos by type
        df['category'] = df['title'].apply(YouTubeDataProcessor.categorize_video_type)
        
        # Categorize videos by duration
        df['duration_category'] = pd.cut(
            df['duration_min'],
            bins=[0, 5, 15, 30, 60, float('inf')],
            labels=['Very Short (<5min)', 'Short (5-15min)', 'Medium (15-30min)', 
                    'Long (30-60min)', 'Very Long (>60min)']
        )
        
        return df


# ============================================================================
# ANALYSIS & VISUALIZATION
# ============================================================================

class YouTubeAnalytics:
    """Class for analyzing YouTube data"""
    
    def __init__(self, df):
        """
        Initialize analytics with dataframe
        
        Args:
            df (pd.DataFrame): Processed video data
        """
        self.df = df
        
    def generate_summary_stats(self):
        """Generate summary statistics for key metrics"""
        numeric_cols = ['views', 'likes', 'comments', 'duration_sec', 
                       'likes_per_view', 'comments_per_view', 'engagement_rate']
        
        summary = self.df[numeric_cols].describe()
        
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(summary.round(2))
        print("\n")
        
        return summary
    
    def analyze_top_videos(self, metric='views', n=10):
        """
        Analyze top performing videos
        
        Args:
            metric (str): Metric to sort by
            n (int): Number of top videos to return
            
        Returns:
            pd.DataFrame: Top videos
        """
        top_videos = self.df.nlargest(n, metric)[
            ['title', 'views', 'likes', 'comments', 'engagement_rate', 
             'duration_min', 'category', 'published']
        ]
        
        print(f"\n{'='*80}")
        print(f"TOP {n} VIDEOS BY {metric.upper()}")
        print(f"{'='*80}\n")
        print(top_videos.to_string(index=False))
        print("\n")
        
        return top_videos
    
    def analyze_keyword_frequency(self, top_percentile=0.1):
        """
        Analyze keyword frequency in top-performing videos
        
        Args:
            top_percentile (float): Percentile of top videos to analyze
            
        Returns:
            list: Most common keywords with counts
        """
        threshold = int(len(self.df) * top_percentile)
        top_videos = self.df.nlargest(threshold, 'views')
        
        # Extract and count keywords
        keywords = []
        for title in top_videos['title']:
            words = re.findall(r'\b\w+\b', title.lower())
            keywords.extend(words)
        
        # Filter out common stop words
        stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 
                     'and', 'or', 'is', 'with', 'from', '|', 'vs', 'by', 'are',
                     'be', 'as', 'it', 'this', 'that', 'my', 'your', 'i', 'you'}
        keywords = [w for w in keywords if w not in stop_words and len(w) > 2]
        
        common_keywords = Counter(keywords).most_common(15)
        
        print(f"\n{'='*80}")
        print(f"MOST COMMON KEYWORDS IN TOP {int(top_percentile*100)}% VIDEOS")
        print(f"{'='*80}\n")
        for word, count in common_keywords:
            print(f"{word:.<30} {count:>4}")
        print("\n")
        
        return common_keywords
    
    def test_duration_engagement_hypothesis(self):
        """
        HYPOTHESIS 1: Test if shorter videos have higher engagement
        
        Returns:
            dict: Test results
        """
        print(f"\n{'='*80}")
        print("HYPOTHESIS TEST 1: Duration vs Engagement")
        print("H0: Video duration has no effect on engagement")
        print("H1: Shorter videos have higher engagement")
        print(f"{'='*80}\n")
        
        # Correlation tests
        corr_likes, p_likes = pearsonr(
            self.df['duration_sec'], 
            self.df['likes_per_view']
        )
        
        corr_comments, p_comments = pearsonr(
            self.df['duration_sec'], 
            self.df['comments_per_view']
        )
        
        corr_engagement, p_engagement = pearsonr(
            self.df['duration_sec'], 
            self.df['engagement_rate']
        )
        
        results = {
            'likes_correlation': corr_likes,
            'likes_p_value': p_likes,
            'comments_correlation': corr_comments,
            'comments_p_value': p_comments,
            'engagement_correlation': corr_engagement,
            'engagement_p_value': p_engagement
        }
        
        print(f"Correlation (Duration vs Likes/View):    {corr_likes:.4f} (p={p_likes:.4f})")
        print(f"Correlation (Duration vs Comments/View): {corr_comments:.4f} (p={p_comments:.4f})")
        print(f"Correlation (Duration vs Engagement):    {corr_engagement:.4f} (p={p_engagement:.4f})")
        
        if p_engagement < 0.05:
            if corr_engagement < 0:
                print(f"\n✓ HYPOTHESIS SUPPORTED: Shorter videos have significantly higher engagement (p<0.05)")
            else:
                print(f"\n✗ HYPOTHESIS REJECTED: Longer videos have higher engagement (p<0.05)")
        else:
            print(f"\n✗ HYPOTHESIS REJECTED: No significant correlation found (p≥0.05)")
            print("   Conclusion: Video duration does not significantly affect engagement")
        
        print("\n")
        return results
    
    def test_day_of_week_hypothesis(self):
        """
        HYPOTHESIS 2: Test if videos published on specific days perform better
        
        Returns:
            dict: Test results
        """
        print(f"\n{'='*80}")
        print("HYPOTHESIS TEST 2: Day of Week vs Performance")
        print("H0: Publishing day has no effect on video views")
        print("H1: Certain days yield significantly higher views")
        print(f"{'='*80}\n")
        
        # Group views by day of week
        day_groups = [
            self.df[self.df['day_of_week'] == i]['views'].values 
            for i in range(7)
        ]
        
        # ANOVA test
        f_stat, p_value = f_oneway(*day_groups)
        
        print(f"ANOVA F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            print(f"\n✓ HYPOTHESIS SUPPORTED: Day of week significantly affects views (p<0.05)")
            print("\nPerforming post-hoc Tukey HSD test to identify specific differences...\n")
            
            # Tukey's HSD test
            tukey = pairwise_tukeyhsd(
                endog=self.df['views'],
                groups=self.df['day_of_week'],
                alpha=0.05
            )
            
            print(tukey.summary())
            
            # Calculate mean views by day
            day_means = self.df.groupby('day_name')['views'].mean().sort_values(ascending=False)
            print(f"\n{'Day':.<20} {'Average Views':>15}")
            print("-"*40)
            for day, views in day_means.items():
                print(f"{day:.<20} {views:>15,.0f}")
            
            best_day = day_means.idxmax()
            worst_day = day_means.idxmin()
            print(f"\n📊 RECOMMENDATION: Publish on {best_day} (avoid {worst_day})")
        else:
            print(f"\n✗ HYPOTHESIS REJECTED: Day of week does not significantly affect views (p≥0.05)")
        
        print("\n")
        
        return {'f_statistic': f_stat, 'p_value': p_value}
    
    def test_tutorial_vs_career_hypothesis(self):
        """
        HYPOTHESIS 3: Test if tutorial videos get more views than career advice videos
        
        Returns:
            dict: Test results including statistics and conclusion
        """
        print(f"\n{'='*80}")
        print("HYPOTHESIS TEST 3: Tutorial vs Career Advice Video Performance")
        print("H0: Tutorial and Career videos have equal average views")
        print("H1: Tutorial videos get significantly more views than Career videos")
        print(f"{'='*80}\n")
        
        # Filter for Tutorial and Career videos
        tutorial_videos = self.df[self.df['category'] == 'Tutorial']
        career_videos = self.df[self.df['category'] == 'Career']
        
        # Check if we have enough data
        if len(tutorial_videos) < 2 or len(career_videos) < 2:
            print("⚠️  Insufficient data for comparison")
            print(f"   Tutorial videos: {len(tutorial_videos)}")
            print(f"   Career videos: {len(career_videos)}")
            return None
        
        # Get view data
        tutorial_views = tutorial_videos['views'].values
        career_views = career_videos['views'].values
        
        # Descriptive statistics
        print(f"Tutorial Videos (n={len(tutorial_videos)}):")
        print(f"  Mean views:   {tutorial_views.mean():>12,.0f}")
        print(f"  Median views: {np.median(tutorial_views):>12,.0f}")
        print(f"  Std dev:      {tutorial_views.std():>12,.0f}")
        
        print(f"\nCareer Videos (n={len(career_videos)}):")
        print(f"  Mean views:   {career_views.mean():>12,.0f}")
        print(f"  Median views: {np.median(career_views):>12,.0f}")
        print(f"  Std dev:      {career_views.std():>12,.0f}")
        
        # Perform both parametric and non-parametric tests
        print(f"\n{'-'*80}")
        print("Statistical Tests:")
        print(f"{'-'*80}")
        
        # 1. Independent samples t-test (parametric)
        t_stat, t_pvalue = ttest_ind(tutorial_views, career_views)
        print(f"\n1. Independent Samples t-test (parametric):")
        print(f"   t-statistic: {t_stat:.4f}")
        print(f"   p-value:     {t_pvalue:.4f}")
        
        # 2. Mann-Whitney U test (non-parametric - more robust for skewed data)
        u_stat, u_pvalue = mannwhitneyu(tutorial_views, career_views, alternative='two-sided')
        print(f"\n2. Mann-Whitney U test (non-parametric - recommended for YouTube data):")
        print(f"   U-statistic: {u_stat:.4f}")
        print(f"   p-value:     {u_pvalue:.4f}")
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt((tutorial_views.std()**2 + career_views.std()**2) / 2)
        cohens_d = (tutorial_views.mean() - career_views.mean()) / pooled_std
        print(f"\n3. Effect Size (Cohen's d): {cohens_d:.4f}")
        
        # Interpret effect size
        if abs(cohens_d) < 0.2:
            effect_interpretation = "negligible"
        elif abs(cohens_d) < 0.5:
            effect_interpretation = "small"
        elif abs(cohens_d) < 0.8:
            effect_interpretation = "medium"
        else:
            effect_interpretation = "large"
        print(f"   Interpretation: {effect_interpretation} effect")
        
        # Determine result based on Mann-Whitney test (more appropriate for this data)
        alpha = 0.05
        print(f"\n{'='*80}")
        print("CONCLUSION:")
        print(f"{'='*80}\n")
        
        if u_pvalue < alpha:
            if tutorial_views.mean() > career_views.mean():
                print(f"✓ HYPOTHESIS SUPPORTED (p={u_pvalue:.4f} < {alpha})")
                print(f"\n  Tutorial videos get SIGNIFICANTLY MORE views than Career videos.")
                diff_percent = ((tutorial_views.mean() - career_views.mean()) / career_views.mean()) * 100
                print(f"  Tutorial videos average {diff_percent:.1f}% more views than Career videos.")
                print(f"  Effect size: {effect_interpretation}")
            else:
                print(f"✗ HYPOTHESIS REJECTED (p={u_pvalue:.4f} < {alpha})")
                print(f"\n  Career videos actually get SIGNIFICANTLY MORE views than Tutorial videos.")
                diff_percent = ((career_views.mean() - tutorial_views.mean()) / tutorial_views.mean()) * 100
                print(f"  Career videos average {diff_percent:.1f}% more views than Tutorial videos.")
        else:
            print(f"✗ HYPOTHESIS REJECTED (p={u_pvalue:.4f} ≥ {alpha})")
            print(f"\n  No significant difference in views between Tutorial and Career videos.")
            print(f"  While Tutorial videos average {tutorial_views.mean():.0f} views vs")
            print(f"  Career videos' {career_views.mean():.0f} views, this difference is not")
            print(f"  statistically significant.")
        
        # Additional insights
        print(f"\n📊 ADDITIONAL INSIGHTS:")
        
        # Engagement comparison
        tutorial_engagement = tutorial_videos['engagement_rate'].mean()
        career_engagement = career_videos['engagement_rate'].mean()
        print(f"  • Tutorial engagement rate: {tutorial_engagement:.4f}")
        print(f"  • Career engagement rate:   {career_engagement:.4f}")
        
        if tutorial_engagement > career_engagement:
            print(f"  • Tutorial videos have {((tutorial_engagement/career_engagement - 1)*100):.1f}% higher engagement")
        else:
            print(f"  • Career videos have {((career_engagement/tutorial_engagement - 1)*100):.1f}% higher engagement")
        
        # Video count comparison
        total_videos = len(tutorial_videos) + len(career_videos)
        tutorial_pct = (len(tutorial_videos) / total_videos) * 100
        career_pct = (len(career_videos) / total_videos) * 100
        print(f"\n  • Tutorial videos: {tutorial_pct:.1f}% of content")
        print(f"  • Career videos:   {career_pct:.1f}% of content")
        
        print("\n")
        
        results = {
            'tutorial_count': len(tutorial_videos),
            'career_count': len(career_videos),
            'tutorial_mean_views': tutorial_views.mean(),
            'career_mean_views': career_views.mean(),
            'tutorial_median_views': np.median(tutorial_views),
            'career_median_views': np.median(career_views),
            't_statistic': t_stat,
            't_pvalue': t_pvalue,
            'u_statistic': u_stat,
            'u_pvalue': u_pvalue,
            'cohens_d': cohens_d,
            'effect_size': effect_interpretation,
            'hypothesis_supported': u_pvalue < alpha and tutorial_views.mean() > career_views.mean()
        }
        
        return results
    
    def compare_video_categories(self):
        """
        Compare performance across all video categories
        
        Returns:
            pd.DataFrame: Category performance metrics
        """
        category_stats = self.df.groupby('category').agg({
            'views': ['mean', 'median', 'sum', 'count'],
            'likes_per_view': 'mean',
            'comments_per_view': 'mean',
            'engagement_rate': 'mean',
            'duration_min': 'mean'
        }).round(2)
        
        print(f"\n{'='*80}")
        print("VIDEO CATEGORY PERFORMANCE ANALYSIS")
        print(f"{'='*80}\n")
        print(category_stats)
        print("\n")
        
        # Perform ANOVA across all categories
        category_groups = [
            self.df[self.df['category'] == cat]['views'].values 
            for cat in self.df['category'].unique()
        ]
        
        f_stat, p_value = f_oneway(*category_groups)
        print(f"ANOVA Test Across All Categories:")
        print(f"  F-statistic: {f_stat:.4f}")
        print(f"  P-value:     {p_value:.4f}")
        
        if p_value < 0.05:
            print(f"  ✓ Significant differences exist between categories (p<0.05)")
        else:
            print(f"  ✗ No significant differences between categories (p≥0.05)")
        
        print("\n")
        
        return category_stats


class YouTubeVisualizer:
    """Class for creating visualizations"""
    
    def __init__(self, df):
        """
        Initialize visualizer with dataframe
        
        Args:
            df (pd.DataFrame): Processed video data
        """
        self.df = df
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def plot_duration_distribution(self, save_path=None):
        """Plot distribution of video durations"""
        plt.figure(figsize=(12, 6))
        
        sns.histplot(self.df['duration_min'], bins=30, kde=True, color='steelblue')
        
        plt.title('Distribution of Video Duration (Minutes)', fontsize=14, fontweight='bold')
        plt.xlabel('Duration (Minutes)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.axvline(self.df['duration_min'].median(), color='red', 
                   linestyle='--', label=f'Median: {self.df["duration_min"].median():.1f} min')
        plt.legend()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_category_comparison(self, save_path=None):
        """
        NEW: Plot comparison of Tutorial vs Career videos
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Filter for Tutorial and Career videos
        tutorial_career = self.df[self.df['category'].isin(['Tutorial', 'Career'])]
        
        # 1. Box plot of views
        sns.boxplot(data=tutorial_career, x='category', y='views', ax=axes[0, 0], palette='Set2')
        axes[0, 0].set_title('View Distribution: Tutorial vs Career', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Views')
        axes[0, 0].set_xlabel('')
        
        # 2. Bar plot of mean views
        category_means = tutorial_career.groupby('category')['views'].mean()
        category_means.plot(kind='bar', ax=axes[0, 1], color=['steelblue', 'coral'], edgecolor='black')
        axes[0, 1].set_title('Average Views: Tutorial vs Career', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Average Views')
        axes[0, 1].set_xlabel('')
        axes[0, 1].tick_params(axis='x', rotation=0)
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(category_means):
            axes[0, 1].text(i, v, f'{v:,.0f}', ha='center', va='bottom')
        
        # 3. Engagement rate comparison
        sns.boxplot(data=tutorial_career, x='category', y='engagement_rate', ax=axes[1, 0], palette='Set3')
        axes[1, 0].set_title('Engagement Rate: Tutorial vs Career', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Engagement Rate')
        axes[1, 0].set_xlabel('')
        
        # 4. Video count
        category_counts = tutorial_career['category'].value_counts()
        category_counts.plot(kind='bar', ax=axes[1, 1], color=['#2ecc71', '#e74c3c'], edgecolor='black')
        axes[1, 1].set_title('Number of Videos: Tutorial vs Career', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Count')
        axes[1, 1].set_xlabel('')
        axes[1, 1].tick_params(axis='x', rotation=0)
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(category_counts):
            axes[1, 1].text(i, v, f'{v}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_correlation_heatmap(self, save_path=None):
        """Plot correlation heatmap of key metrics"""
        metrics = ['views', 'likes', 'comments', 'duration_sec', 
                  'likes_per_view', 'comments_per_view', 'engagement_rate']
        
        corr_matrix = self.df[metrics].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=1,
            cbar_kws={'shrink': 0.8}
        )
        
        plt.title('Correlation Matrix of Video Metrics', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_quarterly_trends(self, save_path=None):
        """Plot quarterly view trends"""
        quarterly_stats = self.df.groupby('upload_quarter').agg({
            'views': 'sum',
            'engagement_rate': 'mean'
        }).reset_index()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Views trend
        ax1.plot(quarterly_stats['upload_quarter'], quarterly_stats['views'], 
                marker='o', linewidth=2, markersize=8, color='steelblue')
        ax1.set_title('Quarterly Total Views Trend', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Quarter', fontsize=12)
        ax1.set_ylabel('Total Views', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Engagement trend
        ax2.plot(quarterly_stats['upload_quarter'], quarterly_stats['engagement_rate'], 
                marker='s', linewidth=2, markersize=8, color='coral')
        ax2.set_title('Quarterly Average Engagement Rate Trend', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Quarter', fontsize=12)
        ax2.set_ylabel('Engagement Rate', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_day_of_week_performance(self, save_path=None):
        """Plot performance by day of week"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Boxplot
        sns.boxplot(data=self.df, x='day_of_week', y='views', 
                   palette='Set2', ax=axes[0])
        axes[0].set_title('View Distribution by Day of Week', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Day of Week', fontsize=12)
        axes[0].set_ylabel('Views', fontsize=12)
        axes[0].set_xticklabels(days, rotation=45)
        
        # Mean views bar chart
        day_means = self.df.groupby('day_name')['views'].mean().reindex(days)
        day_means.plot(kind='bar', ax=axes[1], color='steelblue', edgecolor='black')
        axes[1].set_title('Average Views by Day of Week', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Day of Week', fontsize=12)
        axes[1].set_ylabel('Average Views', fontsize=12)
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_top_keywords(self, keywords, save_path=None):
        """
        Plot top keywords bar chart
        
        Args:
            keywords (list): List of tuples (word, count)
        """
        words, counts = zip(*keywords)
        
        plt.figure(figsize=(12, 6))
        plt.barh(words, counts, color='teal', edgecolor='black')
        plt.xlabel('Frequency', fontsize=12)
        plt.ylabel('Keywords', fontsize=12)
        plt.title('Most Common Keywords in Top-Performing Videos', 
                 fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """Main execution pipeline with all three hypothesis tests"""
    
    print("\n" + "="*80)
    print("YOUTUBE CHANNEL CONTENT ANALYTICS PROJECT")
    print("Channel: Alex The Analyst")
    print("="*80 + "\n")
    
    # 1. CONFIGURATION
    print("Step 1: Configuring YouTube API...")
    config = YouTubeConfig()
    youtube = config.build_youtube_client()
    print("✓ API client configured successfully\n")
    
    # 2. DATA EXTRACTION
    print("Step 2: Extracting video data...")
    extractor = YouTubeDataExtractor(youtube, config.channel_id)
    
    # Get upload playlist
    playlist_id = extractor.get_upload_playlist_id()
    if not playlist_id:
        print("✗ Failed to fetch playlist ID")
        return
    
    # Get all video IDs
    video_ids = extractor.get_all_video_ids(playlist_id)
    if not video_ids:
        print("✗ Failed to fetch video IDs")
        return
    
    # Get video details
    video_data = extractor.get_video_details(video_ids)
    if not video_data:
        print("✗ Failed to fetch video details")
        return
    
    print(f"✓ Data extraction complete\n")
    
    # 3. DATA PROCESSING
    print("Step 3: Processing data...")
    df = pd.DataFrame(video_data)
    df = YouTubeDataProcessor.process_dataframe(df)
    print(f"✓ Processed {len(df)} videos with {len(df.columns)} features\n")
    
    # Save raw data
    output_file = 'youtube_analytics_data_complete.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Data saved to: {output_file}\n")
    
    # 4. ANALYSIS
    print("Step 4: Performing analysis...\n")
    analytics = YouTubeAnalytics(df)
    
    # Generate summary statistics
    analytics.generate_summary_stats()
    
    # Analyze top videos
    analytics.analyze_top_videos(metric='views', n=10)
    analytics.analyze_top_videos(metric='engagement_rate', n=10)
    
    # Keyword analysis
    keywords = analytics.analyze_keyword_frequency(top_percentile=0.1)
    
    # ALL THREE HYPOTHESIS TESTS
    print("\n" + "="*80)
    print("HYPOTHESIS TESTING SECTION")
    print("="*80)
    
    h1_results = analytics.test_duration_engagement_hypothesis()
    h2_results = analytics.test_day_of_week_hypothesis()
    h3_results = analytics.test_tutorial_vs_career_hypothesis()
    
    # Category comparison
    analytics.compare_video_categories()
    
    # 5. VISUALIZATION
    print("Step 5: Creating visualizations...\n")
    visualizer = YouTubeVisualizer(df)
    
    visualizer.plot_duration_distribution(save_path='duration_distribution.png')
    visualizer.plot_correlation_heatmap(save_path='correlation_heatmap.png')
    visualizer.plot_quarterly_trends(save_path='quarterly_trends.png')
    visualizer.plot_day_of_week_performance(save_path='day_of_week_performance.png')
    visualizer.plot_top_keywords(keywords, save_path='top_keywords.png')
    visualizer.plot_category_comparison(save_path='tutorial_vs_career_comparison.png')
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80 + "\n")
    
    # Summary of hypothesis test results
    print("="*80)
    print("HYPOTHESIS TESTING SUMMARY")
    print("="*80)
    print("\nH1: Shorter videos have higher engagement")
    print(f"   Result: {'✓ Supported' if h1_results and h1_results['engagement_p_value'] < 0.05 else '✗ Rejected'}")
    
    print("\nH2: Videos published on specific days perform better")
    print(f"   Result: {'✓ Supported' if h2_results['p_value'] < 0.05 else '✗ Rejected'}")
    
    if h3_results:
        print("\nH3: Tutorial videos get more views than career advice videos")
        print(f"   Result: {'✓ Supported' if h3_results['hypothesis_supported'] else '✗ Rejected'}")
        print(f"   Tutorial mean: {h3_results['tutorial_mean_views']:,.0f} views")
        print(f"   Career mean:   {h3_results['career_mean_views']:,.0f} views")
        print(f"   p-value:       {h3_results['u_pvalue']:.4f}")
    
    print("\n" + "="*80 + "\n")
    
    return df, analytics, visualizer


if __name__ == "__main__":
    df, analytics, visualizer = main()
