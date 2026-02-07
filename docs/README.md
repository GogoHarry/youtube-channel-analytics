# 📊 YouTube Channel Analytics Project

> **A comprehensive data analytics solution for YouTube content optimization**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-success)](https://github.com)

---

## 🎯 Project Overview

This project performs in-depth statistical analysis of YouTube channel performance to identify growth opportunities and optimize content strategy. Using the YouTube Data API v3, it extracts, processes, and analyzes video metrics to provide **actionable, data-driven insights**.

### 🏆 Key Features

- **Automated Data Extraction** - Fetch complete channel history via YouTube API
- **Comprehensive Analysis** - 20+ metrics and derived features
- **Hypothesis Testing** - Statistical validation of content strategies
- **Professional Visualizations** - Publication-ready charts and graphs
- **Keyword Analysis** - Identify winning title patterns
- **Performance Benchmarking** - Compare content categories
- **Temporal Trends** - Track channel growth over time

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Analysis Results](#-analysis-results)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/GogoHarry/youtube-channel-analytics.git
cd youtube-channel-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
echo "API_KEY=your_youtube_api_key" > .env

# 4. Run analysis
python youtube_channel_analytics.py
```

**That's it!** The analysis will run automatically and generate:
- CSV dataset (`youtube_analytics_data.csv`)
- 5 professional visualizations (PNG format)
- Console reports with key insights

---

## 📁 Project Structure

```
youtube-channel-analytics/
│
├── 📄 youtube_channel_analytics.py      # Main analysis script
├── 📄 requirements.txt                  # Python dependencies
├── 📄 .env                              # API credentials (create this)
├── 📄 .gitignore                        # Git ignore rules
│
├── 📂 data/
│   └── youtube_analytics_data.csv       # Extracted dataset
│
├── 📂 visualizations/
│   ├── duration_distribution.png
│   ├── correlation_heatmap.png
│   ├── quarterly_trends.png
│   ├── day_of_week_performance.png
│   └── top_keywords.png
|
├── 📂 notebooks/
│   └── youtube_channel_analytics.ipynb  # Jupyter notebook for exploration
│
└── 📂 docs/
    ├── PROJECT_DOCUMENTATION.md         # Complete project docs
    ├── IMPLEMENTATION_GUIDE.md          # Step-by-step setup
    └── README.md                        # This file
```

---

## 💻 Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **YouTube Data API Key** ([Get One Free](https://console.cloud.google.com/))
- **pip** (Python package installer)

### Step 1: Clone Repository

```bash
git clone https://github.com/GogoHarry/youtube-channel-analytics.git
cd youtube-channel-analytics
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `google-api-python-client` - YouTube API interaction
- `pandas` - Data manipulation
- `matplotlib` & `seaborn` - Visualization
- `scipy` & `statsmodels` - Statistical analysis
- `python-dotenv` - Environment configuration

---

## 🔧 Configuration

### Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create credentials → **API Key**
5. Copy your API key

### Set Up Environment

Create a `.env` file in the project root:

```env
API_KEY=AIzaSyBrUlfBgwuhZ4xS0ScVWXIlGxOYmCuvgXE
```

⚠️ **Security Note:** Never commit `.env` to version control!

### Configure Target Channel (Optional)

To analyze a different channel, modify `youtube_channel_analytics.py`:

```python
class YouTubeConfig:
    def __init__(self):
        # ... other code ...
        self.channel_id = "YOUR_CHANNEL_ID_HERE"
```

---

## 🎮 Usage

### Basic Execution

```bash
python youtube_channel_analytics.py
```

### Expected Output

```
================================================================================
YOUTUBE CHANNEL CONTENT ANALYTICS PROJECT
Channel: Alex The Analyst
================================================================================

Step 1: Configuring YouTube API...
✓ API client configured successfully

Step 2: Extracting video data...
✓ Successfully fetched 356 video IDs
✓ Successfully fetched details for 356 videos
✓ Data extraction complete

Step 3: Processing data...
✓ Processed 356 videos with 20 features
✓ Data saved to: youtube_analytics_data.csv

Step 4: Performing analysis...
[Detailed statistical reports follow]

Step 5: Creating visualizations...
[Generating charts...]

================================================================================
ANALYSIS COMPLETE
================================================================================
```

### Custom Analysis

```python
from youtube_channel_analytics import main

# Run full pipeline
df, analytics, visualizer = main()

# Access data
print(f"Total videos: {len(df)}")
print(f"Average views: {df['views'].mean():,.0f}")

# Custom analysis
top_10 = df.nlargest(10, 'views')
print(top_10[['title', 'views']])

# Additional visualizations
visualizer.plot_duration_distribution()
```

---

## 📊 Analysis Results

### Key Insights Generated

#### 1. **Performance Metrics**
- Total views, likes, comments per video
- Engagement rates (likes/view, comments/view)
- Duration analysis (seconds, minutes, categories)

#### 2. **Temporal Patterns**
- Quarterly view trends
- Best publishing days (ANOVA-validated)
- Month-over-month growth

#### 3. **Content Optimization**
- Top 10 videos by views/engagement
- Keyword frequency in high-performers
- Category performance comparison

#### 4. **Statistical Validation**
- **Hypothesis 1:** Duration vs Engagement (correlation test)
- **Hypothesis 2:** Day of Week vs Performance (ANOVA + Tukey HSD)
- **Hypothesis 3:** Content Category Effectiveness

### Sample Findings

```
================================================================================
TOP 10 VIDEOS BY VIEWS
================================================================================
1. Data Analyst Portfolio Project | SQL       2,128,199 views
2. FREE Data Analyst Bootcamp!!               1,902,963 views
3. SQL Basics Tutorial For Beginners          1,462,657 views
...

================================================================================
PUBLISHING DAY ANALYSIS
================================================================================
Best Day:    Sunday    (186,432 avg views) ✓ Significant (p<0.05)
Worst Day:   Saturday  (31,546 avg views)

================================================================================
TOP KEYWORDS IN HIGH-PERFORMING VIDEOS
================================================================================
data................ 23 occurrences
analyst............. 16 occurrences
beginners........... 12 occurrences
sql................. 10 occurrences
```

---

## 📚 Documentation

### Complete Documentation Suite

| Document | Purpose | Location |
|----------|---------|----------|
| **Project Documentation** | Objectives, methodology, findings | [`docs/PROJECT_DOCUMENTATION.md`](docs/PROJECT_DOCUMENTATION.md) |
| **Implementation Guide** | Step-by-step setup & troubleshooting | [`docs/IMPLEMENTATION_GUIDE.md`](docs/IMPLEMENTATION_GUIDE.md) |
| **Improvements Summary** | Code refactoring details | [`docs/IMPROVEMENTS_SUMMARY.md`](docs/IMPROVEMENTS_SUMMARY.md) |
| **API Reference** | Function documentation | In-code docstrings |

### Quick Links

- 📖 [How to Get YouTube API Key](docs/IMPLEMENTATION_GUIDE.md#step-21-create-google-cloud-project)
- 🐛 [Troubleshooting Guide](docs/IMPLEMENTATION_GUIDE.md#5-troubleshooting)
- 📊 [Understanding Results](docs/IMPLEMENTATION_GUIDE.md#4-understanding-the-output)
- 🔧 [Custom Analysis](docs/IMPLEMENTATION_GUIDE.md#custom-channel-analysis)

---

## 🎨 Visualizations

### Generated Charts

1. **Duration Distribution**
   - Histogram with KDE overlay
   - Shows typical video lengths
   - Identifies outliers

2. **Correlation Heatmap**
   - Views ↔ Likes ↔ Comments
   - Identifies strong relationships
   - Color-coded significance

3. **Quarterly Trends**
   - Total views per quarter
   - Average engagement rate
   - Growth/decline patterns

4. **Day of Week Performance**
   - Boxplot showing distribution
   - Bar chart of average views
   - Statistical significance markers

5. **Top Keywords**
   - Horizontal bar chart
   - Frequency counts
   - Focus on actionable terms

**Example:**

```
Quarterly Views Trend
4,000,000 ┤                 ╭─╮
          │                 │ │
3,000,000 ┤             ╭───╯ ╰─╮
          │             │       │
2,000,000 ┤         ╭───╯       ╰───╮
          │     ╭───╯               │
1,000,000 ┤─────╯                   ╰────────
          └───────────────────────────────────
         2020  2021  2022  2023  2024  2025
```

---

## 🔬 Technical Details

### API Usage

- **Quota Cost:** ~5 units per video
- **Daily Limit:** 10,000 units (free tier)
- **Videos Fetched:** ~2,000 videos per day max
- **Batch Size:** 50 videos per request

### Data Processing

```python
# Key transformations applied:
1. ISO 8601 duration → seconds/minutes
2. Engagement metrics (likes/view, comments/view)
3. Temporal features (quarter, day of week, month)
4. Content categorization (Tutorial, Career, Project, etc.)
5. Duration categories (Short, Medium, Long, etc.)
```

### Statistical Methods

- **Pearson Correlation:** Measures linear relationships
- **One-Way ANOVA:** Tests if group means differ
- **Tukey HSD:** Identifies which groups differ (post-hoc)
- **Descriptive Statistics:** Mean, median, std, quartiles

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to new functions
- Include unit tests (if applicable)
- Update documentation
- Keep commits atomic and descriptive

---

## 📈 Roadmap

### Planned Enhancements

- [ ] **Real-time Dashboard** (Streamlit/Dash)
- [ ] **Sentiment Analysis** on comments
- [ ] **Thumbnail Effectiveness** analysis
- [ ] **Watch Time Prediction** models
- [ ] **Automated Reporting** (weekly email)
- [ ] **Multi-Channel Comparison**
- [ ] **Competitor Benchmarking**

---

## 🙏 Acknowledgments

- **YouTube Data API** - Google for providing free API access
- **Pandas/NumPy** - Open-source data science libraries
- **Matplotlib/Seaborn** - Visualization libraries
- **Alex The Analyst** - Channel used as case study

---

## 📞 Support

### Get Help

- 📖 [Read Documentation](docs/PROJECT_DOCUMENTATION.md)
- 🐛 [Report Issues](https://github.com/GogoHarry/youtube-channel-analytics/issues)
- 💬 [Discussion Forum](https://github.com/GogoHarry/youtube-channel-analytics/discussions)

### Common Issues

| Issue | Solution |
|-------|----------|
| API Key Error | Verify `.env` file exists and contains valid key |
| Quota Exceeded | Wait 24 hours for quota reset |
| Import Errors | Run `pip install -r requirements.txt` |
| No Data Fetched | Check channel ID and API key permissions |

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Gogo Harrison

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🌟 Star History

If this project helped you, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=GogoHarry/youtube-channel-analytics&type=Date)](https://star-history.com/#GogoHarry/youtube-channel-analytics&Date)

---

## 📊 Project Statistics

- **Lines of Code:** 1,200+
- **Functions:** 25+
- **Classes:** 5
- **Test Coverage:** Ready for implementation
- **Documentation:** 100% complete

---

<div align="center">

**Made with ❤️ by [Gogo Harrison](https://github.com/GogoHarry)**

[Documentation](docs/) • [Report Bug](https://github.com/GogoHarry/youtube-channel-analytics/issues) • [Request Feature](https://github.com/GogoHarry/youtube-channel-analytics/issues)

</div>
