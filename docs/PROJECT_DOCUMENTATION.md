# YouTube Channel Content Analytics Project

## 📋 Project Overview

This project performs a comprehensive statistical analysis of the "Alex The Analyst" YouTube channel to identify growth opportunities and optimize content strategy through data-driven insights.

### **Channel Information**
- **Channel Name:** Alex The Analyst
- **Channel ID:** UC7cs8q-gJRlGwj4A8OmCmXg
- **Focus:** Data Analytics Education and Career Guidance
- **Total Videos Analyzed:** 442

---

## 🎯 Project Objectives

### Primary Objectives

1. **Performance Analysis**
   - Identify top-performing videos by views, engagement, and other metrics
   - Understand distribution patterns in video performance
   - Analyze temporal trends in channel growth

2. **Content Strategy Optimization**
   - Determine optimal video duration for maximum engagement
   - Identify best publishing days for maximum reach
   - Analyze keyword effectiveness in high-performing videos
   - Compare performance across different content categories

3. **Hypothesis Testing**
   - **H1:** Shorter videos have higher engagement rates
   - **H2:** Videos published on specific days perform better
   - **H3:** Tutorial videos generate more views than career advice videos

4. **Actionable Insights**
   - Provide data-driven recommendations for content creation
   - Suggest optimal publishing strategies
   - Identify content gaps and opportunities

---

## 🔧 Technical Requirements

### Prerequisites

```bash
# Python Version
Python 3.8+

# Required Libraries
google-api-python-client==2.80.0
google-auth-httplib2==0.1.0
google-auth-oauthlib==1.0.0
pandas==2.0.0
numpy==1.24.0
matplotlib==3.7.0
seaborn==0.12.0
scipy==1.10.0
python-dotenv==1.0.0
statsmodels==0.14.0
```

### Installation

```bash
# Clone repository
git clone https://github.com/GogoHarry/youtube-channel-analytics.git
cd youtube-channel-analytics

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "API_KEY=your_youtube_api_key_here" > .env
```

---

## 📊 Data Collection Methodology

### Step 1: Generate YouTube API Key

1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "YouTube Analytics Project")
3. Enable **YouTube Data API v3**:
   - Click Navigation menu → **API & Services** → **Enable APIs & Services**
   - Search for "YouTube Data API v3"
   - Click **Enable**

4. Create API Credentials:
   - Go to **Credentials** in the sidebar
   - Click **Create Credentials** → **API Key**
   - Copy and securely store the API key

5. Configure API Key:
   ```bash
   # Save in .env file
   API_KEY=AIzaSyBrUlfBgwuhZ4xS0ScVWXIlGxOYmCuvgXE
   ```

### Step 2: Data Extraction Process

#### 2.1 Channel Identification
```python
# Target channel configuration
channel_id = "UC7cs8q-gJRlGwj4A8OmCmXg"  # Alex The Analyst
```

#### 2.2 Upload Playlist Retrieval
- Fetch channel metadata to locate the "Uploads" playlist
- This playlist contains all publicly available videos

#### 2.3 Video ID Collection
- Paginate through playlist items (50 videos per request)
- Extract video IDs for detailed metadata retrieval
- Handle pagination tokens to fetch all videos

#### 2.4 Detailed Metadata Extraction
For each video, retrieve:
- **Snippet Data:**
  - Title
  - Description
  - Published date
  - Tags
  - Channel information

- **Statistics:**
  - View count
  - Like count
  - Comment count

- **Content Details:**
  - Duration (ISO 8601 format)
  - Video definition
  - Caption availability

### Step 3: Data Processing

#### 3.1 Duration Conversion
Convert ISO 8601 duration format to seconds:
```
PT15M30S → 930 seconds
PT1H2M15S → 3735 seconds
```

#### 3.2 Derived Metrics
Calculate engagement indicators:
- `likes_per_view = likes / views`
- `comments_per_view = comments / views`
- `engagement_rate = (likes + comments) / views`

#### 3.3 Temporal Features
Extract time-based attributes:
- Upload quarter (e.g., "2024Q3")
- Day of week (0=Monday, 6=Sunday)
- Month and year

#### 3.4 Content Categorization
Classify videos by type:
- **Tutorial:** Educational content with step-by-step instructions
- **Career:** Job search, salary, interview advice
- **Project:** Portfolio projects and full implementations
- **Tools:** Software-specific tutorials (Excel, SQL, Python, etc.)
- **Q&A/Livestream:** Interactive sessions
- **Advice:** Tips, best practices, recommendations

---

## 📈 Analysis Framework

### 1. Exploratory Data Analysis (EDA)

#### Summary Statistics
Generate descriptive statistics for:
- Views (mean, median, std, quartiles)
- Engagement metrics
- Video duration distribution
- Temporal patterns

#### Distribution Analysis
- **Duration Distribution:** Understand typical video lengths
- **View Distribution:** Identify outliers and patterns
- **Engagement Distribution:** Assess typical interaction rates

### 2. Performance Analysis

#### Top Content Identification
Identify top 10 videos by:
- Total views
- Engagement rate
- Growth velocity (views per day since publish)

#### Keyword Analysis
- Extract keywords from top 10% performing videos
- Count frequency of terms
- Filter common stop words
- Identify successful content themes

### 3. Correlation Analysis

Calculate Pearson correlations between:
- Duration ↔ Views
- Duration ↔ Engagement
- Views ↔ Likes
- Views ↔ Comments

**Interpretation:**
- Strong positive (r > 0.7): Variables increase together
- Weak/None (|r| < 0.3): Little to no relationship
- Strong negative (r < -0.7): Inverse relationship

### 4. Hypothesis Testing

#### Test 1: Duration vs Engagement
**Null Hypothesis (H₀):** Video duration has no effect on engagement  
**Alternative Hypothesis (H₁):** Shorter videos have higher engagement

**Method:** Pearson correlation test
```
Significance Level: α = 0.05
Decision Rule: Reject H₀ if p-value < 0.05
```

#### Test 2: Day of Week vs Performance
**Null Hypothesis (H₀):** Publishing day has no effect on views  
**Alternative Hypothesis (H₁):** Certain days yield higher views

**Method:** One-way ANOVA + Tukey HSD post-hoc
```
Step 1: ANOVA tests if ANY day differs
Step 2: Tukey HSD identifies WHICH days differ
Significance Level: α = 0.05
```

#### Test 3: Tutorial vs Career Advice Video Performance"
**Null Hypothesis (H₀):** Tutorial and Career videos have equal average views  
**Alternative Hypothesis (H₁):** Tutorial videos get significantly more views than Career videos

**Method:** Independent t-test + Mann-Whitney U test + Effect Size (Cohen's d)
```
Step 1: Independent t-test (parametric) tests mean difference
Step 2: Mann-Whitney U test (non-parametric) - PRIMARY test for skewed data
Step 3: Cohen's d measures practical significance
Significance Level: α = 0.05
```

---

## 📊 Key Findings Summary

### 1. Duration Insights
- **Median Duration:** ~12 minutes
- **Most Common Range:** 5-15 minutes
- **Correlation with Engagement:** No significant relationship (p > 0.05)
- **Recommendation:** Focus on content quality over duration constraints

### 2. Publishing Day Analysis
- **Best Day:** Sunday (significantly higher average views)
- **Worst Day:** Saturday (lowest average views)
- **Statistical Significance:** Yes (p < 0.05)
- **Recommendation:** Prioritize Sunday uploads for maximum reach

### 3. Keyword Success Patterns
Top keywords in high-performing videos:
1. **Data** (23 occurrences)
2. **Analyst** (16 occurrences)
3. **Beginners** (12 occurrences)
4. **SQL** (10 occurrences)
5. **Tutorial** (implied in structure)

### 4. Content Category Performance
| Category | Avg Views | Avg Engagement | Recommendation |
|----------|-----------|----------------|----------------|
| Tutorial | High | Medium | Continue focus |
| Career | Medium | High | Increase frequency |
| Project | Very High | High | Priority content |
| Tools | High | Medium | Maintain balance |

### 5. Quarterly Trends
- **Peak Period:** Q1 2021 & Q2 2021 (5M+ total views)
- **Recent Decline:** Significant drop in 2024-2025
- **Potential Causes:** Algorithm changes, content saturation, posting frequency

---

## 💡 Actionable Recommendations

### Content Strategy
1. **Increase Project-Based Content** (highest performance)
2. **Maintain Tutorial Focus** (consistent engagement)
3. **Balance Career Advice** (high engagement rate despite fewer views)
4. **Target Beginner-Friendly Titles** (keyword analysis shows demand)

### Publishing Strategy
1. **Optimal Day:** Upload on Sundays
2. **Avoid:** Saturday uploads
3. **Secondary Options:** Tuesday shows promise

### Duration Strategy
1. **Flexibility:** No significant correlation found
2. **Focus:** Prioritize content completeness over arbitrary time limits
3. **Sweet Spot:** 10-20 minutes appears most common for tutorials

### Keyword Optimization
Include these proven keywords in titles:
- "Data Analyst"
- "Tutorial"
- "Beginners"
- "SQL/Python/Excel" (specific tools)
- "Project/Portfolio"

---

## 🔄 Project Structure

```
youtube-channel-analytics/
│
├── youtube_channel_analytics.py         # Main analysis script
├── requirements.txt                     # Dependencies
├── .env                                 # API credentials (not tracked)
├── .gitignore                           # Git ignore file
│
├── data/  
│   ├── youtube_analytics_data.csv        # Extracted data
│   └── processed_data.csv                # Processed dataset
│
├── visualizations/
│   ├── duration_distribution.png
│   ├── correlation_heatmap.png
│   ├── quarterly_trends.png
│   ├── day_of_week_performance.png
│   └── top_keywords.png
│
├── notebooks/
│   └── youtube_channel_analytics.ipynb     # Jupyter notebook for exploration
│
└── docs/
    ├── PROJECT_DOCUMENTATION.md             # This file
    ├── IMPLEMENTATION_GUIDE.md              # Step-by-step setup    
    └── FINDINGS_AND_RECOMMENDATIONS.md      # Comprehensive findings & Recommendations
```

---

## 🚀 Usage Instructions

### Quick Start

```python
from alex_youtube_analytics import main

# Run complete analysis pipeline
df, analytics, visualizer = main()
```

### Custom Analysis

```python
from alex_youtube_analytics import (
    YouTubeConfig, 
    YouTubeDataExtractor,
    YouTubeDataProcessor,
    YouTubeAnalytics,
    YouTubeVisualizer
)

# 1. Configure API
config = YouTubeConfig()
youtube = config.build_youtube_client()

# 2. Extract Data
extractor = YouTubeDataExtractor(youtube, config.channel_id)
playlist_id = extractor.get_upload_playlist_id()
video_ids = extractor.get_all_video_ids(playlist_id)
video_data = extractor.get_video_details(video_ids)

# 3. Process Data
df = pd.DataFrame(video_data)
df = YouTubeDataProcessor.process_dataframe(df)

# 4. Analyze
analytics = YouTubeAnalytics(df)
analytics.generate_summary_stats()
analytics.test_duration_engagement_hypothesis()
analytics.test_day_of_week_hypothesis()

# 5. Visualize
visualizer = YouTubeVisualizer(df)
visualizer.plot_correlation_heatmap()
visualizer.plot_quarterly_trends()
```

---

## 📝 Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `video_id` | string | Unique YouTube video identifier |
| `title` | string | Video title |
| `views` | integer | Total view count |
| `likes` | integer | Total like count |
| `comments` | integer | Total comment count |
| `duration` | string | ISO 8601 duration format |
| `duration_sec` | integer | Duration in seconds |
| `duration_min` | float | Duration in minutes |
| `published` | datetime | Upload timestamp (UTC) |
| `likes_per_view` | float | Engagement: likes/views ratio |
| `comments_per_view` | float | Engagement: comments/views ratio |
| `engagement_rate` | float | Combined engagement metric |
| `upload_quarter` | string | Quarter of upload (e.g., "2024Q3") |
| `day_of_week` | integer | Day index (0=Monday, 6=Sunday) |
| `day_name` | string | Day name (e.g., "Sunday") |
| `category` | string | Content category classification |

---

## 🔬 **Statistical Methods**

### **Pearson Correlation**
Measures linear relationship between two continuous variables.

**Formula:**
```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]
```

**Interpretation:**
- r = 1: Perfect positive correlation
- r = 0: No correlation
- r = -1: Perfect negative correlation

---

### **One-Way ANOVA**
Tests if means differ across multiple groups.

**Hypotheses:**
- H₀: μ₁ = μ₂ = ... = μₖ (all means equal)
- H₁: At least one mean differs

**Test Statistic:** F-ratio

**Decision:** Reject H₀ if p-value < α

---

### **Tukey's HSD (Honest Significant Difference)**
Post-hoc test identifying which specific groups differ.

**Purpose:** Control family-wise error rate in multiple comparisons

**Output:** Pairwise comparisons with adjusted p-values

---

### **Independent Samples t-test**
Tests if means differ between two independent groups (parametric test).

**Hypotheses:**
- H₀: μ₁ = μ₂ (means are equal)
- H₁: μ₁ ≠ μ₂ (means differ)

**Formula:**
```
t = (x̄₁ - x̄₂) / √[(s₁²/n₁) + (s₂²/n₂)]
```

**Assumptions:**
- Independent samples
- Normally distributed data (or large sample size)
- Homogeneity of variance (or use Welch's t-test)

**Decision:** Reject H₀ if p-value < α

---

### **Mann-Whitney U Test**
Non-parametric alternative to independent t-test for comparing two groups.

**Hypotheses:**
- H₀: Distributions are equal
- H₁: One distribution tends to have larger values

**Advantages:**
- Does not assume normal distribution
- More robust for skewed data (e.g., YouTube view counts)
- Better handles outliers

**Test Statistic:** U-statistic (sum of ranks)

**Decision:** Reject H₀ if p-value < α

**Use Case:** Primary test for Hypothesis 3 due to highly skewed YouTube data distribution

---

### **Cohen's d (Effect Size)**
Measures the standardized difference between two group means.

**Formula:**
```
d = (μ₁ - μ₂) / σ_pooled

where: σ_pooled = √[(σ₁² + σ₂²) / 2]
```

**Interpretation:**
- |d| < 0.2: Negligible effect
- |d| < 0.5: Small effect
- |d| < 0.8: Medium effect
- |d| ≥ 0.8: Large effect

**Purpose:** Assesses practical significance beyond statistical significance

**Note:** Cohen's d complements p-values by indicating whether a statistically significant difference is also meaningfully large

---

## 🛡️ Limitations & Considerations

1. **API Quota Limits**
   - YouTube API has daily quota restrictions
   - Large channels may require multiple days for full data extraction

2. **Historical Bias**
   - Older videos have more time to accumulate views
   - Recent uploads may show artificially low performance

3. **External Factors**
   - Algorithm changes not captured in data
   - Seasonal trends may affect results
   - Cross-promotion and external traffic not tracked

4. **Engagement Limitations**
   - Dislikes no longer publicly available (removed by YouTube)
   - Watch time data not accessible via API
   - Subscriber conversion rates unknown

---

## 🔮 Future Enhancements

1. **Advanced Analytics**
   - Sentiment analysis of comments
   - Thumbnail effectiveness analysis (requires computer vision)
   - Watch time prediction models

2. **Automation**
   - Scheduled data updates
   - Real-time dashboard with Streamlit/Dash
   - Automated reporting email system

3. **Comparative Analysis**
   - Benchmark against similar channels
   - Industry trend analysis
   - Competitive positioning

4. **Machine Learning**
   - View count prediction models
   - Content recommendation engine
   - Optimal posting time predictor

---

## 📚 References

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Statistical Analysis with SciPy](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Seaborn Visualization Gallery](https://seaborn.pydata.org/examples/index.html)

---

## 📧 Contact & Support

**Project Maintainer:** Gogo Harrison  
**Email:** gogoharrison66@gmail.com  
**GitHub:** [github.com/GogoHarry/youtube-channel-analytics](https://github.com/GogoHarry/youtube-channel-analytics)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated:** February 2026
