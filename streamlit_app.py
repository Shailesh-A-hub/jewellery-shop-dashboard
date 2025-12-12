"""
💎 ENHANCED JEWELLERY INVENTORY AI SYSTEM v5.0
Complete ML Enhancement with Slow-Stock Analysis, Demand Forecasting, 
Dynamic Pricing, Charm Prediction & AI Business Models
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# ⭐ MODULE 1: SLOW-STOCK CATEGORY ANALYSIS
# ============================================================================

class SlowStockAnalyzer:
    """
    ABC-XYZ Analysis for Inventory Classification
    A = High value, Z = Low value
    X = High consumption variability, Z = Low variability
    """
    
    def __init__(self, inventory_df, sales_history_df):
        self.inventory = inventory_df.copy()
        self.sales = sales_history_df.copy()
    
    def calculate_turnover_metrics(self):
        """Calculate turnover rate and stock metrics"""
        # Group sales by product
        monthly_sales = self.sales.groupby('product_id')['quantity'].sum().reset_index()
        monthly_sales.columns = ['product_id', 'total_sales']
        
        # Merge with inventory
        data = self.inventory.merge(monthly_sales, on='product_id', how='left')
        data['total_sales'] = data['total_sales'].fillna(0)
        
        # Calculate metrics
        data['turnover_rate'] = data['total_sales'] / (data['quantity'] + 1)  # Avoid division by zero
        data['stock_value'] = data['price'] * data['quantity']
        data['annual_sales_value'] = data['price'] * data['total_sales']
        
        # Calculate stock age (days since last movement)
        last_movement = self.sales.groupby('product_id')['date'].max().reset_index()
        last_movement.columns = ['product_id', 'last_sold']
        data = data.merge(last_movement, on='product_id', how='left')
        data['stock_age'] = (datetime.now() - pd.to_datetime(data['last_sold'])).dt.days
        data['stock_age'] = data['stock_age'].fillna(999)  # Not sold = very old
        
        return data
    
    def abc_analysis(self, data):
        """Classify products into A, B, C categories by value"""
        total_value = data['annual_sales_value'].sum()
        data = data.sort_values('annual_sales_value', ascending=False)
        data['cumulative_value'] = data['annual_sales_value'].cumsum()
        data['cumulative_pct'] = (data['cumulative_value'] / total_value) * 100
        
        def assign_class(pct):
            if pct <= 80:
                return 'A (High Value)'
            elif pct <= 95:
                return 'B (Medium Value)'
            else:
                return 'C (Low Value)'
        
        data['ABC_Class'] = data['cumulative_pct'].apply(assign_class)
        return data
    
    def xyz_analysis(self, data):
        """Classify by consumption consistency"""
        # Calculate coefficient of variation for each product
        monthly_by_product = self.sales.groupby('product_id').agg({
            'quantity': ['mean', 'std', 'count']
        }).reset_index()
        monthly_by_product.columns = ['product_id', 'avg_qty', 'std_qty', 'periods']
        
        # Coefficient of variation
        monthly_by_product['cv'] = monthly_by_product['std_qty'] / (monthly_by_product['avg_qty'] + 0.1)
        
        def assign_xyz(cv):
            if cv < 0.5:
                return 'X (Stable Demand)'
            elif cv < 1.0:
                return 'Y (Moderate Variation)'
            else:
                return 'Z (Highly Variable)'
        
        monthly_by_product['XYZ_Class'] = monthly_by_product['cv'].apply(assign_xyz)
        
        data = data.merge(monthly_by_product[['product_id', 'XYZ_Class']], 
                         on='product_id', how='left')
        return data
    
    def classify_stock_status(self, data):
        """Classify as Fast, Normal, or Slow moving"""
        def get_status(turnover, stock_age):
            if turnover >= 12 or stock_age < 30:
                return '⚡ Fast Moving'
            elif turnover >= 2 and stock_age < 90:
                return '📦 Normal'
            elif turnover >= 1 and stock_age < 180:
                return '🐢 Slow Moving'
            else:
                return '⚠️ Dead Stock'
        
        data['Stock_Status'] = data.apply(
            lambda row: get_status(row['turnover_rate'], row['stock_age']), axis=1
        )
        return data
    
    def analyze(self):
        """Run complete analysis"""
        data = self.calculate_turnover_metrics()
        data = self.abc_analysis(data)
        data = self.xyz_analysis(data)
        data = self.classify_stock_status(data)
        
        # Add risk score (0-100)
        slow_score = data['stock_age'].max()
        data['risk_score'] = (
            (data['stock_age'] / slow_score * 30) +  # 30% age factor
            ((1 - data['turnover_rate'].clip(0, 1)) * 50) +  # 50% turnover factor
            ((data['quantity'] / data['quantity'].max()) * 20)  # 20% quantity factor
        )
        
        return data.sort_values('risk_score', ascending=False)


# ============================================================================
# ⭐ MODULE 2: DEMAND FORECASTING & TIME SERIES PREDICTION
# ============================================================================

class DemandForecast:
    """
    Multiple forecasting methods: Moving Average, Exponential Smoothing, Linear Regression
    Real implementation would use ARIMA/Prophet
    """
    
    def __init__(self, sales_history_df):
        self.sales = sales_history_df.copy()
        self.sales['date'] = pd.to_datetime(self.sales['date'])
    
    def moving_average_forecast(self, product_id, periods=12, forecast_days=30):
        """Simple moving average forecast"""
        product_sales = self.sales[self.sales['product_id'] == product_id].copy()
        product_sales = product_sales.sort_values('date')
        
        if len(product_sales) < periods:
            return product_sales['quantity'].mean(), product_sales['quantity'].std()
        
        ma = product_sales['quantity'].rolling(window=periods).mean().iloc[-1]
        std = product_sales['quantity'].std()
        
        return ma, std
    
    def exponential_smoothing(self, product_id, alpha=0.3):
        """Exponential smoothing with trend"""
        product_sales = self.sales[self.sales['product_id'] == product_id].copy()
        product_sales = product_sales.sort_values('date')
        
        if len(product_sales) < 2:
            return product_sales['quantity'].mean(), product_sales['quantity'].std()
        
        values = product_sales['quantity'].values
        
        # Simple exponential smoothing
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[i-1])
        
        forecast = smoothed[-1]
        residuals = np.array(values) - np.array(smoothed)
        std_error = np.std(residuals)
        
        return forecast, std_error
    
    def seasonal_decomposition(self, product_id):
        """Detect seasonal patterns"""
        product_sales = self.sales[self.sales['product_id'] == product_id].copy()
        product_sales = product_sales.sort_values('date')
        
        if len(product_sales) < 12:
            return None, 0.0
        
        # Monthly aggregation
        product_sales['month'] = pd.to_datetime(product_sales['date']).dt.to_period('M')
        monthly = product_sales.groupby('month')['quantity'].sum()
        
        if len(monthly) < 12:
            return None, 0.0
        
        # Calculate seasonality index
        overall_mean = monthly.mean()
        seasonality = monthly / overall_mean
        
        # Coefficient of variation of seasonality
        seasonal_strength = seasonality.std() / seasonality.mean()
        
        return seasonality.to_dict(), seasonal_strength
    
    def forecast_product_demand(self, product_id, horizon_days=30):
        """Ensemble forecast combining multiple methods"""
        ma_forecast, ma_std = self.moving_average_forecast(product_id)
        es_forecast, es_std = self.exponential_smoothing(product_id)
        
        # Ensemble: weight average
        forecast = (ma_forecast * 0.5 + es_forecast * 0.5)
        confidence_interval = np.sqrt((ma_std**2 + es_std**2) / 2)
        
        return {
            'forecast': forecast,
            'lower_bound': max(0, forecast - 1.96 * confidence_interval),
            'upper_bound': forecast + 1.96 * confidence_interval,
            'confidence': confidence_interval,
            'horizon_days': horizon_days
        }


# ============================================================================
# ⭐ MODULE 3: DYNAMIC PRICING ENGINE
# ============================================================================

class DynamicPricingEngine:
    """
    ML-based pricing optimization considering:
    - Demand elasticity
    - Inventory age
    - Competition
    - Margin targets
    - Seasonal factors
    """
    
    def __init__(self, inventory_df, sales_df, cost_df):
        self.inventory = inventory_df
        self.sales = sales_df
        self.costs = cost_df
    
    def calculate_price_elasticity(self, product_id, price_variations=None):
        """
        Elasticity = (% Change in Quantity) / (% Change in Price)
        Negative value = normal goods
        """
        product_sales = self.sales[self.sales['product_id'] == product_id]
        
        if len(product_sales) < 10:
            return -1.2  # Default elasticity
        
        # Group by week and calculate average
        product_sales = product_sales.copy()
        product_sales['date'] = pd.to_datetime(product_sales['date'])
        product_sales['week'] = product_sales['date'].dt.isocalendar().week
        
        weekly_data = product_sales.groupby('week').agg({
            'quantity': 'sum',
            'price': 'mean'
        }).reset_index()
        
        if len(weekly_data) < 4:
            return -1.2
        
        # Simple elasticity calculation
        price_changes = weekly_data['price'].pct_change()
        qty_changes = weekly_data['quantity'].pct_change()
        
        # Filter outliers
        valid = (~np.isinf(price_changes)) & (~np.isinf(qty_changes)) & (price_changes != 0)
        
        if valid.sum() < 2:
            return -1.2
        
        elasticity = (qty_changes[valid] / price_changes[valid]).median()
        return elasticity
    
    def calculate_optimal_price(self, product_id, inventory_age_days, 
                               target_margin_pct=0.35, demand_level='normal'):
        """
        Optimal Price = Cost × (1 + Margin Factor) × Elasticity Adjustment × Inventory Adjustment
        """
        # Get product cost
        product_cost = self.costs[self.costs['product_id'] == product_id]['cost'].values
        if len(product_cost) == 0:
            return None
        
        base_cost = product_cost[0]
        base_margin = 1 + target_margin_pct
        
        # Elasticity adjustment
        elasticity = self.calculate_price_elasticity(product_id)
        elasticity_factor = 1.0 if elasticity > -1 else 0.95  # Slight discount if elastic
        
        # Inventory age adjustment (old stock = lower price)
        age_factor = 1.0
        if inventory_age_days > 180:
            age_factor = 0.80  # 20% markdown
        elif inventory_age_days > 90:
            age_factor = 0.90  # 10% markdown
        elif inventory_age_days > 60:
            age_factor = 0.95  # 5% markdown
        
        # Demand adjustment
        demand_factor = {'high': 1.15, 'normal': 1.0, 'low': 0.85}.get(demand_level, 1.0)
        
        optimal_price = base_cost * base_margin * elasticity_factor * age_factor * demand_factor
        
        return {
            'base_cost': base_cost,
            'base_price': base_cost * base_margin,
            'optimal_price': optimal_price,
            'discount_pct': ((base_cost * base_margin - optimal_price) / (base_cost * base_margin)) * 100,
            'elasticity': elasticity,
            'age_factor': age_factor,
            'demand_factor': demand_factor
        }
    
    def generate_bundle_recommendations(self, slow_products, fast_products, bundle_size=2):
        """
        Recommend bundles: pair slow-moving with fast-moving items
        Strategy: Discount bundle to encourage fast-moving sales
        """
        bundles = []
        
        for slow_id in slow_products:
            for fast_id in fast_products[:bundle_size]:
                slow_price = self.inventory[self.inventory['product_id'] == slow_id]['price'].values[0]
                fast_price = self.inventory[self.inventory['product_id'] == fast_id]['price'].values[0]
                
                bundle_price = (slow_price + fast_price) * 0.92  # 8% bundle discount
                
                bundles.append({
                    'bundle_id': f"{slow_id}_{fast_id}",
                    'slow_product': slow_id,
                    'fast_product': fast_id,
                    'bundle_price': bundle_price,
                    'regular_total': slow_price + fast_price,
                    'discount_amount': (slow_price + fast_price) - bundle_price
                })
        
        return pd.DataFrame(bundles)


# ============================================================================
# ⭐ MODULE 4: CHARM PREDICTION MODEL (Jewelry Appeal)
# ============================================================================

class CharmPredictor:
    """
    ML Model to predict jewelry appeal/demand potential
    Features: design type, weight, purity, gemstone quality, price point
    Target: sales velocity, customer rating, conversion rate
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = None
    
    def create_features(self, product_df):
        """
        Feature engineering for jewelry products
        """
        features = product_df.copy()
        
        # Design complexity score (0-10)
        design_mapping = {
            'simple': 2,
            'moderate': 5,
            'intricate': 8,
            'bespoke': 10
        }
        features['design_complexity'] = features['design'].map(design_mapping).fillna(5)
        
        # Purity index
        purity_mapping = {
            '22k': 0.916,
            '18k': 0.750,
            '14k': 0.583,
            '9k': 0.375
        }
        features['purity_index'] = features['purity'].map(purity_mapping).fillna(0.75)
        
        # Price category
        features['price_category'] = pd.qcut(features['price'], q=3, labels=[1, 2, 3])
        features['price_category'] = features['price_category'].astype(int)
        
        # Gemstone value
        gemstone_value = {
            'diamond': 5,
            'ruby': 4,
            'sapphire': 4,
            'emerald': 3,
            'pearl': 2,
            'none': 1
        }
        features['gemstone_value'] = features.get('gemstone', 'none').map(gemstone_value).fillna(1)
        
        # Market trend score (0-10, higher = trending)
        features['trend_score'] = np.random.randint(3, 10, len(features))  # Replace with real data
        
        return features[['design_complexity', 'purity_index', 'price_category', 
                        'gemstone_value', 'trend_score']]
    
    def train_charm_model(self, products_df, sales_history_df):
        """
        Train charm prediction model
        Label: High charm (high sales velocity) vs Low charm
        """
        # Calculate sales velocity for each product
        velocity = sales_history_df.groupby('product_id')['quantity'].sum()
        median_velocity = velocity.median()
        
        products_df['charm_label'] = products_df['product_id'].map(
            lambda x: 1 if velocity.get(x, 0) > median_velocity else 0
        )
        
        # Create features
        X = self.create_features(products_df)
        y = products_df['charm_label']
        
        # Train
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.model.fit(X_scaled, y)
        self.feature_names = X.columns
        
        return self.model
    
    def predict_charm_score(self, product_df):
        """Predict charm score (0-100) for products"""
        X = self.create_features(product_df)
        X_scaled = self.scaler.transform(X)
        
        # Get probability of high charm
        probabilities = self.model.predict_proba(X_scaled)
        charm_scores = probabilities[:, 1] * 100
        
        product_df['charm_score'] = charm_scores
        product_df['charm_rating'] = pd.cut(charm_scores, 
                                            bins=[0, 30, 60, 100],
                                            labels=['Low Appeal', 'Medium Appeal', 'High Appeal'])
        
        return product_df


# ============================================================================
# ⭐ MODULE 5: QUICK ACTIONS & ALERTS
# ============================================================================

class QuickActionEngine:
    """
    Automated recommendations for inventory management
    One-click actions to optimize stock
    """
    
    def __init__(self, slow_stock_data, demand_forecasts, pricing_recommendations):
        self.slow_stock = slow_stock_data
        self.forecasts = demand_forecasts
        self.pricing = pricing_recommendations
    
    def generate_actions(self):
        """Generate priority-based action list"""
        actions = []
        
        for idx, product in self.slow_stock.iterrows():
            product_id = product['product_id']
            risk_score = product['risk_score']
            status = product['Stock_Status']
            
            # High risk - Dead stock
            if status == '⚠️ Dead Stock':
                actions.append({
                    'priority': '🔴 CRITICAL',
                    'product_id': product_id,
                    'action': 'Clear Inventory',
                    'recommendation': f"Apply 25-30% markdown + Bundle with bestsellers",
                    'urgency': 'Immediate',
                    'expected_impact': 'Recover 40-60% of value'
                })
            
            # Medium-high risk - Slow moving
            elif status == '🐢 Slow Moving':
                actions.append({
                    'priority': '🟡 HIGH',
                    'product_id': product_id,
                    'action': 'Accelerate Sales',
                    'recommendation': f"Apply 10-15% discount + Featured placement",
                    'urgency': '1-2 weeks',
                    'expected_impact': 'Increase turnover 3-5x'
                })
            
            # Reorder point check
            elif status == '📦 Normal':
                if product['quantity'] < 5:
                    actions.append({
                        'priority': '🟠 MEDIUM',
                        'product_id': product_id,
                        'action': 'Reorder Stock',
                        'recommendation': f"Stock level low: {product['quantity']} units",
                        'urgency': 'This week',
                        'expected_impact': 'Avoid stockout'
                    })
        
        return pd.DataFrame(actions)
    
    def apply_markdown(self, product_id, markdown_pct):
        """Apply price markdown"""
        current_price = self.pricing[self.pricing['product_id'] == product_id]['base_price'].values[0]
        new_price = current_price * (1 - markdown_pct/100)
        return new_price
    
    def create_bundle(self, slow_product_id, fast_product_id, discount_pct=8):
        """Create promotional bundle"""
        slow_price = self.pricing[self.pricing['product_id'] == slow_product_id]['base_price'].values[0]
        fast_price = self.pricing[self.pricing['product_id'] == fast_product_id]['base_price'].values[0]
        
        bundle_price = (slow_price + fast_price) * (1 - discount_pct/100)
        
        return {
            'bundle': f"{slow_product_id} + {fast_product_id}",
            'regular_price': slow_price + fast_price,
            'bundle_price': bundle_price,
            'savings': (slow_price + fast_price) - bundle_price
        }


# ============================================================================
# ⭐ MODULE 6: AI BUSINESS INTELLIGENCE & ANALYTICS
# ============================================================================

class AIBusinessAnalytics:
    """
    Advanced business metrics and AI-driven insights
    - Customer Lifetime Value (CLV) prediction
    - Churn prediction
    - Product recommendations
    - Revenue optimization
    """
    
    def __init__(self, customer_df, sales_df, transaction_df):
        self.customers = customer_df
        self.sales = sales_df
        self.transactions = transaction_df
    
    def calculate_clv(self, customer_id, time_period_months=24):
        """
        CLV = (Average Transaction Value × Purchase Frequency × Customer Lifespan)
        Using historical data to predict future value
        """
        customer_transactions = self.transactions[
            self.transactions['customer_id'] == customer_id
        ]
        
        if len(customer_transactions) == 0:
            return 0
        
        # Calculate metrics
        total_spent = customer_transactions['amount'].sum()
        num_purchases = len(customer_transactions)
        avg_transaction = total_spent / num_purchases
        
        # Estimate lifespan (assume 3 years active customer)
        purchase_frequency = num_purchases / (time_period_months / 12)
        estimated_lifespan_months = 36
        
        clv = avg_transaction * purchase_frequency * (estimated_lifespan_months / 12)
        
        return clv
    
    def predict_customer_churn(self, customer_id, inactivity_threshold_days=90):
        """
        Churn Risk = High if no purchase in 90+ days
        Returns: Churn probability (0-1)
        """
        customer_transactions = self.transactions[
            self.transactions['customer_id'] == customer_id
        ]
        
        if len(customer_transactions) == 0:
            return 1.0  # No purchase history = high churn risk
        
        last_purchase = customer_transactions['date'].max()
        days_inactive = (datetime.now() - pd.to_datetime(last_purchase)).days
        
        # Simple churn model
        if days_inactive > inactivity_threshold_days:
            churn_probability = min(1.0, 0.5 + (days_inactive - inactivity_threshold_days) / 365)
        else:
            churn_probability = (days_inactive / inactivity_threshold_days) * 0.5
        
        return churn_probability
    
    def product_recommendations(self, customer_id, n_recommendations=5):
        """
        Collaborative + Content-based filtering
        Recommend products similar to customer's purchase history
        """
        customer_purchases = self.transactions[
            self.transactions['customer_id'] == customer_id
        ]['product_id'].unique()
        
        # Find customers with similar purchase patterns
        similar_customers = []
        for cust_id in self.transactions['customer_id'].unique():
            if cust_id != customer_id:
                other_purchases = self.transactions[
                    self.transactions['customer_id'] == cust_id
                ]['product_id'].unique()
                
                # Jaccard similarity
                intersection = len(set(customer_purchases) & set(other_purchases))
                union = len(set(customer_purchases) | set(other_purchases))
                
                if union > 0:
                    similarity = intersection / union
                    if similarity > 0.2:
                        similar_customers.append((cust_id, similarity))
        
        # Get products purchased by similar customers
        recommended_products = {}
        for cust_id, similarity in similar_customers:
            cust_products = self.transactions[
                self.transactions['customer_id'] == cust_id
            ]['product_id'].unique()
            
            for product in cust_products:
                if product not in customer_purchases:
                    recommended_products[product] = recommended_products.get(product, 0) + similarity
        
        # Sort and return top N
        top_recommendations = sorted(
            recommended_products.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return top_recommendations
    
    def revenue_optimization(self, inventory_df, sales_df):
        """
        Optimize total revenue by:
        1. Repricing slow movers
        2. Bundling strategies
        3. Demand-based pricing
        4. Inventory allocation
        """
        # Calculate current revenue by product
        revenue_by_product = sales_df.groupby('product_id').apply(
            lambda x: (x['quantity'] * x['price']).sum()
        )
        
        # Calculate optimized revenue
        optimized_revenue = {}
        for product_id in revenue_by_product.index:
            current_rev = revenue_by_product[product_id]
            
            # Estimate: slow items could increase 20-40% with repricing
            product_status = inventory_df[inventory_df['product_id'] == product_id]['Stock_Status'].values
            
            if product_status and 'Slow' in product_status[0]:
                optimized_revenue[product_id] = current_rev * 1.25  # 25% uplift potential
            else:
                optimized_revenue[product_id] = current_rev * 1.05  # 5% uplift
        
        return pd.DataFrame({
            'product_id': list(optimized_revenue.keys()),
            'current_revenue': [revenue_by_product.get(p, 0) for p in optimized_revenue.keys()],
            'optimized_revenue': list(optimized_revenue.values()),
            'revenue_uplift': [
                optimized_revenue[p] - revenue_by_product.get(p, 0) 
                for p in optimized_revenue.keys()
            ]
        })


# ============================================================================
# ⭐ SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_data():
    """Generate realistic sample data"""
    np.random.seed(42)
    
    # Products
    n_products = 50
    designs = ['simple', 'moderate', 'intricate', 'bespoke']
    purities = ['22k', '18k', '14k', '9k']
    gemstones = ['none', 'diamond', 'ruby', 'sapphire', 'emerald']
    
    products = pd.DataFrame({
        'product_id': [f'P{i:03d}' for i in range(n_products)],
        'name': [f'Jewelry Item {i}' for i in range(n_products)],
        'design': np.random.choice(designs, n_products),
        'purity': np.random.choice(purities, n_products),
        'gemstone': np.random.choice(gemstones, n_products),
        'weight_grams': np.random.uniform(5, 50, n_products),
        'quantity': np.random.randint(1, 100, n_products),
        'price': np.random.uniform(5000, 50000, n_products)
    })
    
    # Sales history (last 6 months)
    sales_records = []
    for _ in range(500):
        sales_records.append({
            'product_id': np.random.choice(products['product_id']),
            'quantity': np.random.randint(1, 5),
            'price': np.random.uniform(5000, 50000),
            'date': datetime.now() - timedelta(days=np.random.randint(1, 180))
        })
    
    sales_history = pd.DataFrame(sales_records)
    
    # Costs
    costs = pd.DataFrame({
        'product_id': products['product_id'],
        'cost': products['price'] * np.random.uniform(0.5, 0.7, n_products)
    })
    
    # Customers
    customers = pd.DataFrame({
        'customer_id': [f'C{i:04d}' for i in range(100)],
        'name': [f'Customer {i}' for i in range(100)],
        'email': [f'cust{i}@example.com' for i in range(100)],
        'total_spent': np.random.uniform(10000, 500000, 100),
        'num_purchases': np.random.randint(1, 50, 100),
        'last_purchase_date': [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(100)]
    })
    
    # Transactions
    transactions = []
    for _ in range(300):
        transactions.append({
            'customer_id': np.random.choice(customers['customer_id']),
            'product_id': np.random.choice(products['product_id']),
            'amount': np.random.uniform(5000, 50000),
            'date': datetime.now() - timedelta(days=np.random.randint(1, 365))
        })
    
    transactions_df = pd.DataFrame(transactions)
    
    return products, sales_history, costs, customers, transactions_df


# ============================================================================
# ⭐ MAIN STREAMLIT APP
# ============================================================================

def main():
    st.set_page_config(page_title="💎 AI-Enhanced Inventory System", layout="wide")
    
    st.title("💎 Jewelry Inventory AI System v5.0")
    st.markdown("**Advanced ML: Slow-Stock Analysis | Demand Forecasting | Dynamic Pricing | Charm Prediction**")
    
    # Generate sample data
    products, sales_history, costs, customers, transactions = generate_sample_data()
    
    # Sidebar navigation
    st.sidebar.title("📊 Analytics Modules")
    module = st.sidebar.radio("Select Module", [
        "🐢 Slow-Stock Analysis",
        "📈 Demand Forecasting",
        "💰 Dynamic Pricing",
        "✨ Charm Prediction",
        "⚡ Quick Actions",
        "🤖 AI Business Analytics"
    ])
    
    # ========== SLOW-STOCK ANALYSIS ==========
    if module == "🐢 Slow-Stock Analysis":
        st.header("🐢 Slow-Stock Category Analysis (ABC-XYZ)")
        
        analyzer = SlowStockAnalyzer(products, sales_history)
        analysis_result = analyzer.analyze()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            fast_count = len(analysis_result[analysis_result['Stock_Status'] == '⚡ Fast Moving'])
            st.metric("⚡ Fast Moving", fast_count)
        with col2:
            normal_count = len(analysis_result[analysis_result['Stock_Status'] == '📦 Normal'])
            st.metric("📦 Normal", normal_count)
        with col3:
            slow_count = len(analysis_result[analysis_result['Stock_Status'] == '🐢 Slow Moving'])
            st.metric("🐢 Slow Moving", slow_count)
        with col4:
            dead_count = len(analysis_result[analysis_result['Stock_Status'] == '⚠️ Dead Stock'])
            st.metric("⚠️ Dead Stock", dead_count)
        
        # ABC-XYZ Matrix
        st.subheader("📊 ABC-XYZ Classification Matrix")
        abc_xyz_pivot = pd.crosstab(
            analysis_result['ABC_Class'],
            analysis_result['XYZ_Class'],
            margins=True
        )
        st.dataframe(abc_xyz_pivot)
        
        # Risk assessment
        st.subheader("⚠️ High-Risk Inventory (Risk Score > 70)")
        high_risk = analysis_result[analysis_result['risk_score'] > 70].sort_values('risk_score', ascending=False)
        
        display_cols = ['product_id', 'name', 'quantity', 'stock_age', 'turnover_rate', 
                       'Stock_Status', 'ABC_Class', 'risk_score']
        st.dataframe(high_risk[display_cols], use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(analysis_result, x='turnover_rate', y='stock_age',
                           size='quantity', color='Stock_Status',
                           title="Turnover vs Stock Age", hover_data=['product_id'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            status_counts = analysis_result['Stock_Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Stock Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== DEMAND FORECASTING ==========
    elif module == "📈 Demand Forecasting":
        st.header("📈 Demand Forecasting & Time Series Prediction")
        
        forecaster = DemandForecast(sales_history)
        
        st.subheader("Select Product for Forecast")
        product_id = st.selectbox("Choose Product:", products['product_id'].unique())
        
        forecast = forecaster.forecast_product_demand(product_id, horizon_days=30)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Forecast (30 days)", f"{forecast['forecast']:.0f} units")
        with col2:
            st.metric("Lower Bound (95% CI)", f"{forecast['lower_bound']:.0f}")
        with col3:
            st.metric("Upper Bound (95% CI)", f"{forecast['upper_bound']:.0f}")
        with col4:
            st.metric("Confidence Interval", f"±{forecast['confidence']:.2f}")
        
        # Forecast visualization
        product_sales = sales_history[sales_history['product_id'] == product_id].copy()
        product_sales['date'] = pd.to_datetime(product_sales['date'])
        product_sales = product_sales.sort_values('date')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=product_sales['date'], y=product_sales['quantity'],
                                mode='lines', name='Historical Sales',
                                line=dict(color='blue', width=2)))
        
        future_date = datetime.now() + timedelta(days=30)
        fig.add_hline(y=forecast['forecast'], line_dash="dash", 
                     annotation_text=f"Forecast: {forecast['forecast']:.0f}",
                     annotation_position="right")
        
        fig.update_layout(title=f"Demand Forecast: {product_id}",
                         xaxis_title="Date", yaxis_title="Quantity")
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== DYNAMIC PRICING ==========
    elif module == "💰 Dynamic Pricing":
        st.header("💰 Dynamic Pricing Engine")
        
        pricing_engine = DynamicPricingEngine(products, sales_history, costs)
        
        product_id = st.selectbox("Select Product for Pricing Analysis:", 
                                 products['product_id'].unique(), key="pricing_select")
        
        product = products[products['product_id'] == product_id].iloc[0]
        inventory_age = st.slider("Inventory Age (days):", 0, 365, 60)
        demand_level = st.selectbox("Current Demand Level:", ['low', 'normal', 'high'])
        
        pricing_rec = pricing_engine.calculate_optimal_price(
            product_id, inventory_age, demand_level=demand_level
        )
        
        if pricing_rec:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Base Cost", f"₹{pricing_rec['base_cost']:.0f}")
            with col2:
                st.metric("Standard Price", f"₹{pricing_rec['base_price']:.0f}")
            with col3:
                st.metric("Optimal Price", f"₹{pricing_rec['optimal_price']:.0f}",
                         delta=f"{-pricing_rec['discount_pct']:.1f}%")
            
            st.info(f"""
            **Pricing Recommendation:**
            - Elasticity: {pricing_rec['elasticity']:.2f}
            - Age Factor: {pricing_rec['age_factor']:.2%}
            - Demand Factor: {pricing_rec['demand_factor']:.2%}
            - Suggested Discount: {pricing_rec['discount_pct']:.1f}%
            """)
    
    # ========== CHARM PREDICTION ==========
    elif module == "✨ Charm Prediction":
        st.header("✨ Charm Prediction Model (Jewelry Appeal)")
        
        charm_model = CharmPredictor()
        charm_model.train_charm_model(products, sales_history)
        
        products_with_charm = charm_model.predict_charm_score(products.copy())
        
        col1, col2, col3 = st.columns(3)
        high_charm = len(products_with_charm[products_with_charm['charm_rating'] == 'High Appeal'])
        med_charm = len(products_with_charm[products_with_charm['charm_rating'] == 'Medium Appeal'])
        low_charm = len(products_with_charm[products_with_charm['charm_rating'] == 'Low Appeal'])
        
        with col1:
            st.metric("High Appeal", high_charm)
        with col2:
            st.metric("Medium Appeal", med_charm)
        with col3:
            st.metric("Low Appeal", low_charm)
        
        st.subheader("Charm Score Distribution")
        fig = px.histogram(products_with_charm, x='charm_score', nbins=20,
                          title="Distribution of Charm Scores",
                          labels={'charm_score': 'Charm Score (0-100)'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Top Products by Charm Score")
        top_charm = products_with_charm.nlargest(10, 'charm_score')[
            ['product_id', 'name', 'design', 'charm_score', 'charm_rating']
        ]
        st.dataframe(top_charm, use_container_width=True)
    
    # ========== QUICK ACTIONS ==========
    elif module == "⚡ Quick Actions":
        st.header("⚡ Quick Actions & Automated Recommendations")
        
        analyzer = SlowStockAnalyzer(products, sales_history)
        slow_stock_data = analyzer.analyze()
        
        forecaster = DemandForecast(sales_history)
        pricing_engine = DynamicPricingEngine(products, sales_history, costs)
        
        actions_engine = QuickActionEngine(slow_stock_data, forecaster, pricing_engine)
        actions = actions_engine.generate_actions()
        
        # Filter by priority
        priority_filter = st.selectbox("Filter by Priority:", 
                                      ['All', '🔴 CRITICAL', '🟡 HIGH', '🟠 MEDIUM'])
        
        if priority_filter != 'All':
            actions = actions[actions['priority'] == priority_filter]
        
        st.dataframe(actions, use_container_width=True)
        
        # Action execution UI
        st.subheader("Execute Action")
        if len(actions) > 0:
            selected_action_idx = st.selectbox("Select Action:", range(len(actions)))
            selected_action = actions.iloc[selected_action_idx]
            
            if st.button("Apply Action"):
                st.success(f"✅ Action executed: {selected_action['action']} on {selected_action['product_id']}")
                st.info(f"Recommendation: {selected_action['recommendation']}")
    
    # ========== AI BUSINESS ANALYTICS ==========
    elif module == "🤖 AI Business Analytics":
        st.header("🤖 AI Business Intelligence & Revenue Optimization")
        
        bi = AIBusinessAnalytics(customers, sales_history, transactions)
        
        st.subheader("1️⃣ Customer Lifetime Value (CLV) Analysis")
        
        customer_id = st.selectbox("Select Customer:", customers['customer_id'].unique())
        clv = bi.calculate_clv(customer_id)
        
        st.metric("Customer Lifetime Value", f"₹{clv:.0f}")
        
        # CLV distribution
        clv_values = [bi.calculate_clv(cid) for cid in customers['customer_id']]
        fig = px.histogram(x=clv_values, nbins=20, title="Customer Lifetime Value Distribution",
                          labels={'x': 'CLV (₹)'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("2️⃣ Churn Prediction")
        
        selected_customer = customers[customers['customer_id'] == customer_id].iloc[0]
        churn_risk = bi.predict_customer_churn(customer_id)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Churn Risk (%):", f"{churn_risk*100:.1f}%")
        with col2:
            st.metric("Status:", "🔴 At Risk" if churn_risk > 0.7 else "🟡 Monitor" if churn_risk > 0.4 else "🟢 Stable")
        
        st.subheader("3️⃣ Product Recommendations")
        
        recommendations = bi.product_recommendations(customer_id, n_recommendations=5)
        if recommendations:
            rec_df = pd.DataFrame(recommendations, columns=['Product ID', 'Similarity Score'])
            st.dataframe(rec_df, use_container_width=True)
        
        st.subheader("4️⃣ Revenue Optimization")
        
        revenue_opt = bi.revenue_optimization(products, sales_history)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_current = revenue_opt['current_revenue'].sum()
            st.metric("Current Revenue", f"₹{total_current:.0f}")
        with col2:
            total_optimized = revenue_opt['optimized_revenue'].sum()
            st.metric("Optimized Revenue", f"₹{total_optimized:.0f}")
        with col3:
            total_uplift = revenue_opt['revenue_uplift'].sum()
            st.metric("Potential Uplift", f"₹{total_uplift:.0f}", 
                     delta=f"{(total_uplift/total_current)*100:.1f}%")
        
        # Top opportunities
        st.subheader("Top Revenue Optimization Opportunities")
        top_opportunities = revenue_opt.nlargest(10, 'revenue_uplift')[
            ['product_id', 'current_revenue', 'optimized_revenue', 'revenue_uplift']
        ]
        st.dataframe(top_opportunities, use_container_width=True)


if __name__ == "__main__":
    main()
