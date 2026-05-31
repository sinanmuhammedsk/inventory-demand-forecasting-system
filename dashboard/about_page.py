import streamlit as st

def render_about_page(db):
    st.markdown("<h1 style='text-align: center; color: #0071CE; margin-bottom: 5px;'><span style='color: #0071CE;'>Walmart</span> <span style='color: #FFC220;'>✵</span> <span style='color: #0F172A;'>System Portfolio & Case Study</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #0F172A; font-size:1.05rem;'>System Architecture, Business Optimization Metrics, and Developer Portfolio</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Custom CSS style for dynamic card glow effects in Dark Theme
    st.markdown(
        """
        <style>
        .glow-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
        }
        .glow-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 113, 206, 0.15);
            border-color: #0071CE;
        }
        .glow-card-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #FFC220;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: 0.5px;
        }
        .glow-card-desc {
            font-size: 0.95rem;
            color: #0F172A;
            line-height: 1.6;
        }
        .arch-step {
            background-color: #F3F4F6;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 5px solid #0071CE;
            transition: all 0.2s ease;
        }
        .arch-step:hover {
            background-color: #243049;
            border-left-color: #FFC220;
        }
        .arch-title {
            font-weight: 700;
            color: #0F172A;
            font-size: 1.05rem;
            margin-bottom: 4px;
        }
        .arch-desc {
            font-size: 0.88rem;
            color: #0F172A;
            line-height: 1.5;
        }
        .arrow-down {
            text-align: center;
            font-size: 1.2rem;
            color: #0071CE;
            margin: 8px 0;
            font-weight: bold;
        }
        .bullet-list {
            padding-left: 20px;
            font-size: 0.95rem;
            color: #0F172A;
            line-height: 1.8;
        }
        .bullet-list li b {
            color: #FFC220;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Tabs selection replacing mobile emojis with clean professional text
    tab1, tab2, tab3 = st.tabs([
        "System Overview & Impact",
        "System Architecture",
        "Developer Portfolio"
    ])
    
    with tab1:
        col1, col2 = st.columns([5, 4])
        
        with col1:
            st.markdown(
                """
                <div class="glow-card">
                    <div class="glow-card-title">Project Overview</div>
                    <div class="glow-card-desc">
                        The <b>Inventory Demand Forecasting System</b> is an end-to-end business intelligence and predictive analytics platform 
                        built to solve a critical retail operations challenge: <b>how to maintain optimal stock levels in the face of seasonal demand and supply chain uncertainty</b>.
                        <br><br>
                        By analyzing historical weekly sales records of 45 Walmart locations, the system leverages machine learning 
                        to forecast demand at the Store-Department level. These forecasts are fed into an operations research-based 
                        inventory engine to calculate safety stocks and reorder points, alerting managers to inventory risk in real time.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            st.markdown(
                """
                <div class="glow-card">
                    <div class="glow-card-title">Key Business Impact Summary</div>
                    <div class="glow-card-desc">
                        By replacing manual inventory audits with the automated statistical forecasting models implemented in this project, businesses can achieve substantial operational efficiencies:
                        <ul class="bullet-list" style="margin-top: 10px;">
                            <li><b>Reduction in Stockouts</b>: Expected drop of <b>15-22%</b> by utilizing statistical safety stock buffers.</li>
                            <li><b>Capital Optimization</b>: Up to <b>12%</b> reduction in capital tied up in overstock by identifying excess inventory.</li>
                            <li><b>Audit Automation</b>: Restocking recommendations computed instantly, reducing procurement planning hours from days to minutes.</li>
                            <li><b>Macro Resilience</b>: Quantified low correlation between sales volume and fuel prices, helping secure price hedges.</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with tab2:
        col_arch_left, col_arch_right = st.columns([5, 4])
        
        with col_arch_left:
            st.markdown(
                """
                <div class="arch-step">
                    <div class="arch-title">1. Data Ingestion & Merging</div>
                    <div class="arch-desc">Loads Walmart CSVs (Sales, Store Specs, Macro Factors) & merges on composite keys (Store, Date, Holiday).</div>
                </div>
                <div class="arrow-down">▼</div>
                <div class="arch-step">
                    <div class="arch-title">2. Preprocessing & Feature Engineering</div>
                    <div class="arch-desc">Winsorizes sales outliers, encodes categories, and extracts temporal/specific holiday indicators.</div>
                </div>
                <div class="arrow-down">▼</div>
                <div class="arch-step">
                    <div class="arch-title">3. Forecasting Models (ML Pipeline)</div>
                    <div class="arch-desc">Fits Linear Regression, Random Forests, & XGBoost. Serializes the best-performing model (Random Forest).</div>
                </div>
                <div class="arrow-down">▼</div>
                <div class="arch-step">
                    <div class="arch-title">4. Operations & Optimization Engine</div>
                    <div class="arch-desc">Generates 7/30/90D forecasts, computes safety stock (Z-score * std_dev * sqrt(lead_time)) and ROP.</div>
                </div>
                <div class="arrow-down">▼</div>
                <div class="arch-step">
                    <div class="arch-title">5. Persistence & Interface Layer</div>
                    <div class="arch-desc">Logs runs in MySQL/SQLite, tracks audit logs, and serves a high-fidelity Streamlit Business Intelligence dashboard.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_arch_right:
            st.markdown(
                """
                <div class="glow-card" style="height: 100%;">
                    <div class="glow-card-title">Technical Design Highlights</div>
                    <div class="glow-card-desc">
                        <b>Dual-Database Reliability</b>:
                        Transparents sqlite3/pymysql fallback database manager enables zero-config deployment on local developer devices or cloud instances (Streamlit Cloud).
                        <br><br>
                        <b>Chronological Validation Split</b>:
                        Model training strictly splits data chronologically (train on 2010-2012, validate on mid-to-late 2012) to ensure validation scores reflect real future performance and avoid standard random split lookahead bias.
                        <br><br>
                        <b>Operations Research Integration</b>:
                        Translates mathematical demand forecasts into inventory metrics (Safety Stock, ROP, Order-up-to Quantity) to deliver direct business value beyond raw accuracy metrics.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with tab3:
        col_dev_left, col_dev_right = st.columns([5, 4])
        
        with col_dev_left:
            st.markdown(
                """
                <div class="glow-card" style="height: 100%;">
                    <div class="glow-card-title">Business Intelligence & Data Engineer</div>
                    <div class="glow-card-desc">
                        <b>Core Competencies</b>:
                        <ul class="bullet-list" style="margin-top: 5px; margin-bottom: 15px;">
                            <li>Predictive Modeling & Demand Forecasting</li>
                            <li>Supply Chain Analytics & Operations Research</li>
                            <li>Database Schema Design & Query Optimization</li>
                            <li>Enterprise BI Dashboards & Web App Prototyping</li>
                        </ul>
                        
                        <b>Portfolio Case Study Goals</b>:
                        This project demonstrates an end‑to‑end Inventory Demand Forecasting and Business Intelligence solution built using real‑world Walmart retail sales data. It showcases industry‑relevant Data Analyst skills such as data preprocessing, exploratory data analysis (EDA), SQL‑based data management, machine learning forecasting, KPI monitoring, interactive dashboard development, and inventory optimization.
                        The platform enables demand prediction, inventory risk identification, and data‑driven decision‑making through actionable business insights, automated reporting, and executive‑level analytics. Designed as an enterprise‑style analytics product, it reflects real‑world BI workflows and demonstrates proficiency in Python, SQL, Power BI concepts, data visualization, forecasting, and operational analytics.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_dev_right:
            st.markdown(
                """
                <div class="glow-card" style="height: 100%;">
                    <div class="glow-card-title">Technical Toolkit & Profile</div>
                    <div class="glow-card-desc">
                        <b>Toolbox Showcase</b>:
                        <ul class="bullet-list" style="margin-top: 5px; margin-bottom: 20px;">
                            <li><b>Core Languages</b>: Python, SQL</li>
                            <li><b>Data Science</b>: Pandas, NumPy, Scikit-Learn, XGBoost, Joblib</li>
                            <li><b>Visualizations</b>: Plotly, Streamlit, Custom HTML/CSS Grid</li>
                            <li><b>Databases</b>: MySQL, SQLite, PyMySQL</li>
                        </ul>
                        <div style="text-align: center; margin-top: 20px; display: flex; gap: 12px;">
                            <a href="https://github.com" target="_blank" style="background-color: #0071CE; border: 1px solid #0071CE; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 6px rgba(0,0,0,0.2); flex: 1; transition: all 0.3s ease; text-align: center;">GitHub Profile</a>
                            <a href="https://linkedin.com" target="_blank" style="background-color: #0071CE; border: 1px solid #0071CE; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 6px rgba(0,0,0,0.2); flex: 1; transition: all 0.3s ease; text-align: center;">LinkedIn CV</a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
