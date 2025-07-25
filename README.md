# 🏎️ F1 Statistics Dashboard

A comprehensive Formula 1 statistics dashboard built with Streamlit, featuring race results, qualifying analysis, driver/constructor standings, and detailed circuit information with official F1 team colors throughout.

## 🚀 Features

### **Core Navigation**
- **Smart Season Selection**: Defaults to 2025 British Grand Prix, other years default to Round 1
- **Top Navigation**: Clean, modern interface with season and race selection at the top
- **Intelligent Defaults**: Context-aware race selection based on season

### **Race Analysis**
- **Race Statistics Cards**: Winner, pole position, fastest lap, and fastest pit stop with team colors
- **Qualifying Analysis**: Session best times, lap time comparisons, and qualifying progression
- **Race Results**: Complete race results with team information and status
- **Pit Stop Analysis**: Detailed pit stop comparisons and timing analysis
- **Position Progression**: Visual tracking of driver positions throughout the race

### **Championship Standings**
- **Driver Standings**: Points progression, race wins, podium finishes, and points distribution
- **Constructor Standings**: Team championship analysis with official F1 colors
- **Interactive Charts**: All graphs use official F1 team colors for instant recognition

### **Circuit Information**
- **Circuit Layouts**: High-quality circuit layout images
- **Circuit Details**: Location, country, length, coordinates, and altitude
- **Local Images**: Fast-loading local circuit images with fallback support

### **Visual Design**
- **Official F1 Team Colors**: Every chart, graph, and card uses authentic F1 team colors
- **Consistent Styling**: Professional appearance with uniform card heights and layouts
- **Responsive Design**: Optimized for different screen sizes

## 📁 Project Structure

```
FORMULA 1/
├── app.py                    # Main Streamlit application with top navigation
├── config.py                 # Page configuration and custom CSS styling
├── data_loader.py            # Data loading utilities with race ordering
├── race_display.py           # Main race page display and circuit information
├── race_stats.py             # Race statistics cards with team colors
├── qualifying.py             # Qualifying analysis and session comparisons
├── card_styling.py           # Team-colored card styling utilities
├── graph_styling.py          # Chart styling with official F1 team colors
├── team_colors.py            # Official F1 team color definitions
├── dataframe_styles.py       # Data table styling and formatting
├── utils.py                  # Utility functions for data processing
├── requirements.txt          # Python package dependencies
├── f1_data/                  # F1 CSV data files
│   ├── races.csv
│   ├── drivers.csv
│   ├── constructors.csv
│   ├── results.csv
│   ├── qualifying.csv
│   ├── driver_standings.csv
│   ├── constructor_standings.csv
│   ├── circuits_with_local_images.csv
│   └── ... (other F1 data files)
└── images/                   # Local image assets
    ├── circuit_layouts/      # Circuit layout images
    ├── country_flags/        # 3D country flag images
    ├── circuit_image_mapping.json
    └── flag_image_mapping.json
```

## 🏃‍♂️ Quick Start

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Installation**

1. **Clone or Download** the project files

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**: The app will automatically open at `http://localhost:8501`

### **Alternative Installation**:
```bash
pip install streamlit pandas plotly numpy
streamlit run app.py
```

## 🎯 Usage

1. **Select Season**: Choose an F1 season from the sidebar dropdown
2. **Select Race**: Pick any race from that season
3. **View Information**: See circuit details, race statistics, and results

## 📊 Data Sources

- **F1 Data**: Comprehensive F1 database with races, drivers, constructors, and results
- **Circuit Images**: Official F1 circuit layouts and Wikipedia sources
- **Country Flags**: 3D flag images from cdn.countryflags.com

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Data Processing**: Pandas
- **Grid Display**: streamlit-aggrid
- **Image Storage**: Local file system for fast loading
- **Caching**: Streamlit's built-in caching for optimal performance

## 📈 Statistics Available

- Race winners and podium finishers
- Pole position holders
- Fastest lap times
- Championship standings
- Constructor results
- Qualifying results
- Sprint race results (where applicable)

---

Built with ❤️ for Formula 1 fans
## 🎯 Us
age Guide

### **Navigation**
1. **Select Season**: Choose from available F1 seasons (defaults to 2025)
2. **Select Race**: Pick a specific race (defaults to British GP for 2025, Round 1 for others)
3. **Explore Tabs**: Navigate through Qualifying, Race Results, Driver Standings, etc.

### **Key Features**
- **Team Color Recognition**: All charts use official F1 team colors for easy identification
- **Comprehensive Analysis**: From qualifying sessions to championship standings
- **Interactive Charts**: Hover over charts for detailed information
- **Consistent Design**: Professional F1 broadcast-quality appearance

## 🛠️ Technical Details

### **Dependencies**
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy**: Numerical computing support

### **Data Sources**
- Official F1 CSV data files with race results, qualifying times, and standings
- Circuit information with layouts and specifications
- Driver and constructor data with team affiliations

### **Performance Features**
- **Caching**: Streamlit caching for fast data loading
- **Local Images**: Optimized local image storage for quick loading
- **Efficient Rendering**: Optimized chart rendering with team colors

## 🎨 Design Features

### **Official F1 Team Colors**
- Ferrari: #DC143C (Red)
- Red Bull Racing: #0600EF (Blue)
- Mercedes: #00D2BE (Teal)
- McLaren: #FF8700 (Orange)
- Aston Martin: #006F62 (Green)
- Alpine: #0090FF (Blue)
- Williams: #005AFF (Blue)
- And all other F1 teams with authentic colors

### **Visual Consistency**
- Uniform card heights (150px) for all race statistics
- Consistent typography and spacing throughout
- Professional color scheme matching F1 broadcasts
- Responsive design for different screen sizes

## 🔧 Customization

### **Adding New Seasons**
1. Add new race data to the CSV files in `f1_data/`
2. Update circuit information if needed
3. The dashboard will automatically detect new seasons

### **Modifying Team Colors**
- Edit `team_colors.py` to update or add team colors
- Colors are automatically applied across all charts and cards

### **Custom Styling**
- Modify `config.py` for global styling changes
- Update `card_styling.py` for card-specific styling
- Adjust `graph_styling.py` for chart appearance

## 📊 Data Structure

The dashboard uses standard F1 data format with the following key files:
- `races.csv`: Race information and calendar
- `results.csv`: Race results and finishing positions
- `qualifying.csv`: Qualifying session times
- `drivers.csv`: Driver information and details
- `constructors.csv`: Team/constructor information
- `driver_standings.csv`: Championship standings by driver
- `constructor_standings.csv`: Championship standings by team

## 🚀 Future Enhancements

Potential improvements and features:
- Real-time data integration
- Weather information for races
- Lap-by-lap analysis
- Driver comparison tools
- Historical trend analysis
- Mobile app version

## 📝 License

This project is for educational and personal use. F1 data and team colors are used for informational purposes only.

## 🏁 Enjoy the Dashboard!

Experience Formula 1 like never before with comprehensive statistics, beautiful visualizations, and official team colors throughout. Perfect for F1 fans, analysts, and anyone interested in motorsport data! 🏎️✨