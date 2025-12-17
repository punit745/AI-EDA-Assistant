"""
Model Training Module
Provides comprehensive machine learning model training and evaluation.
Includes regression, classification, and time series models.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score, classification_report
)
from typing import Dict, Tuple, Optional, List
import warnings
warnings.filterwarnings('ignore')

# Import gradient boosting libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False

# Import time series libraries
try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


class ModelTrainer:
    """Train and evaluate machine learning models."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model_type = None
    
    def prepare_data(self, target_column: str, feature_columns: Optional[List[str]] = None, 
                     test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """
        Prepare data for training by splitting into train and test sets.
        
        Args:
            target_column: Name of the target column
            feature_columns: List of feature columns. If None, use all columns except target.
            test_size: Proportion of data to use for testing
            random_state: Random state for reproducibility
            
        Returns:
            Tuple: (X_train, X_test, y_train, y_test)
        """
        if target_column not in self.df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        # Select features
        if feature_columns is None:
            feature_columns = [col for col in self.df.columns if col != target_column]
        
        # Only use numerical columns
        numerical_features = self.df[feature_columns].select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numerical_features) == 0:
            raise ValueError("No numerical features found for training")
        
        X = self.df[numerical_features].dropna()
        y = self.df.loc[X.index, target_column]
        
        # Remove rows where target is NaN
        valid_indices = y.notna()
        X = X[valid_indices]
        y = y[valid_indices]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_linear_regression(self) -> Dict:
        """
        Train a Linear Regression model.
        
        Returns:
            Dict: Training results and metrics
        """
        self.model = LinearRegression()
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        # Metrics
        results = {
            'model_name': 'Linear Regression',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'feature_importance': dict(zip(self.X_train.columns, self.model.coef_))
        }
        
        return results
    
    def train_decision_tree(self, task_type: str = 'regression', max_depth: int = 5) -> Dict:
        """
        Train a Decision Tree model.
        
        Args:
            task_type: 'regression' or 'classification'
            max_depth: Maximum depth of the tree
            
        Returns:
            Dict: Training results and metrics
        """
        if task_type == 'regression':
            self.model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
            self.model_type = 'regression'
        else:
            self.model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'Decision Tree Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'Decision Tree Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def train_random_forest(self, task_type: str = 'regression', n_estimators: int = 100, max_depth: int = 5) -> Dict:
        """
        Train a Random Forest model.
        
        Args:
            task_type: 'regression' or 'classification'
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of each tree
            
        Returns:
            Dict: Training results and metrics
        """
        if task_type == 'regression':
            self.model = RandomForestRegressor(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'regression'
        else:
            self.model = RandomForestClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        # Predictions
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'Random Forest Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'Random Forest Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def cross_validate(self, cv: int = 5) -> Dict:
        """
        Perform cross-validation on the trained model.
        
        Args:
            cv: Number of cross-validation folds
            
        Returns:
            Dict: Cross-validation scores
        """
        if self.model is None:
            raise ValueError("No model has been trained yet")
        
        if self.model_type == 'regression':
            scoring = 'r2'
        else:
            scoring = 'accuracy'
        
        cv_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=cv, scoring=scoring)
        
        return {
            'cv_scores': cv_scores.tolist(),
            'mean_cv_score': cv_scores.mean(),
            'std_cv_score': cv_scores.std()
        }
    
    # ========== ADDITIONAL REGRESSION MODELS ==========
    
    def train_lasso_regression(self, alpha: float = 1.0) -> Dict:
        """
        Train a Lasso Regression model.
        
        Args:
            alpha: Regularization strength
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = Lasso(alpha=alpha, random_state=42)
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'Lasso Regression',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'feature_importance': dict(zip(self.X_train.columns, self.model.coef_)),
            'alpha': alpha
        }
    
    def train_ridge_regression(self, alpha: float = 1.0) -> Dict:
        """
        Train a Ridge Regression model.
        
        Args:
            alpha: Regularization strength
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = Ridge(alpha=alpha, random_state=42)
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'Ridge Regression',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'feature_importance': dict(zip(self.X_train.columns, self.model.coef_)),
            'alpha': alpha
        }
    
    def train_svr(self, kernel: str = 'rbf', C: float = 1.0) -> Dict:
        """
        Train a Support Vector Regression model.
        
        Args:
            kernel: Kernel type ('linear', 'rbf', 'poly')
            C: Regularization parameter
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = SVR(kernel=kernel, C=C)
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'Support Vector Regression',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'kernel': kernel,
            'C': C
        }
    
    def train_knn_regressor(self, n_neighbors: int = 5) -> Dict:
        """
        Train a K-Nearest Neighbors Regression model.
        
        Args:
            n_neighbors: Number of neighbors
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = KNeighborsRegressor(n_neighbors=n_neighbors, n_jobs=-1)
        self.model_type = 'regression'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'K-Nearest Neighbors Regressor',
            'train_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                'mae': mean_absolute_error(self.y_train, y_train_pred),
                'r2_score': r2_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                'mae': mean_absolute_error(self.y_test, y_test_pred),
                'r2_score': r2_score(self.y_test, y_test_pred)
            },
            'n_neighbors': n_neighbors
        }
    
    # ========== CLASSIFICATION MODELS ==========
    
    def train_logistic_regression(self, C: float = 1.0) -> Dict:
        """
        Train a Logistic Regression model.
        
        Args:
            C: Inverse of regularization strength
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = LogisticRegression(C=C, random_state=42, max_iter=1000, n_jobs=-1)
        self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'Logistic Regression',
            'train_metrics': {
                'accuracy': accuracy_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'accuracy': accuracy_score(self.y_test, y_test_pred)
            },
            'feature_importance': dict(zip(self.X_train.columns, self.model.coef_[0] if len(self.model.coef_) == 1 else self.model.coef_.mean(axis=0))),
            'C': C
        }
    
    def train_svc(self, kernel: str = 'rbf', C: float = 1.0) -> Dict:
        """
        Train a Support Vector Classification model.
        
        Args:
            kernel: Kernel type ('linear', 'rbf', 'poly')
            C: Regularization parameter
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = SVC(kernel=kernel, C=C, random_state=42)
        self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'Support Vector Classification',
            'train_metrics': {
                'accuracy': accuracy_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'accuracy': accuracy_score(self.y_test, y_test_pred)
            },
            'kernel': kernel,
            'C': C
        }
    
    def train_knn_classifier(self, n_neighbors: int = 5) -> Dict:
        """
        Train a K-Nearest Neighbors Classification model.
        
        Args:
            n_neighbors: Number of neighbors
            
        Returns:
            Dict: Training results and metrics
        """
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, n_jobs=-1)
        self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        return {
            'model_name': 'K-Nearest Neighbors Classifier',
            'train_metrics': {
                'accuracy': accuracy_score(self.y_train, y_train_pred)
            },
            'test_metrics': {
                'accuracy': accuracy_score(self.y_test, y_test_pred)
            },
            'n_neighbors': n_neighbors
        }
    
    # ========== GRADIENT BOOSTING MODELS ==========
    
    def train_xgboost(self, task_type: str = 'regression', n_estimators: int = 100, 
                     max_depth: int = 5, learning_rate: float = 0.1) -> Dict:
        """
        Train an XGBoost model.
        
        Args:
            task_type: 'regression' or 'classification'
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            
        Returns:
            Dict: Training results and metrics
        """
        if not XGBOOST_AVAILABLE:
            return {'error': 'XGBoost is not installed. Install with: pip install xgboost'}
        
        if task_type == 'regression':
            self.model = xgb.XGBRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'regression'
        else:
            self.model = xgb.XGBClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                n_jobs=-1
            )
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'XGBoost Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'XGBoost Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def train_lightgbm(self, task_type: str = 'regression', n_estimators: int = 100,
                      max_depth: int = 5, learning_rate: float = 0.1) -> Dict:
        """
        Train a LightGBM model.
        
        Args:
            task_type: 'regression' or 'classification'
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            
        Returns:
            Dict: Training results and metrics
        """
        if not LIGHTGBM_AVAILABLE:
            return {'error': 'LightGBM is not installed. Install with: pip install lightgbm'}
        
        if task_type == 'regression':
            self.model = lgb.LGBMRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            self.model_type = 'regression'
        else:
            self.model = lgb.LGBMClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'LightGBM Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'LightGBM Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    def train_catboost(self, task_type: str = 'regression', n_estimators: int = 100,
                      max_depth: int = 5, learning_rate: float = 0.1) -> Dict:
        """
        Train a CatBoost model.
        
        Args:
            task_type: 'regression' or 'classification'
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            
        Returns:
            Dict: Training results and metrics
        """
        if not CATBOOST_AVAILABLE:
            return {'error': 'CatBoost is not installed. Install with: pip install catboost'}
        
        if task_type == 'regression':
            self.model = cb.CatBoostRegressor(
                iterations=n_estimators,
                depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                verbose=0
            )
            self.model_type = 'regression'
        else:
            self.model = cb.CatBoostClassifier(
                iterations=n_estimators,
                depth=max_depth,
                learning_rate=learning_rate,
                random_state=42,
                verbose=0
            )
            self.model_type = 'classification'
        
        self.model.fit(self.X_train, self.y_train)
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        if task_type == 'regression':
            results = {
                'model_name': 'CatBoost Regressor',
                'train_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_train, y_train_pred)),
                    'mae': mean_absolute_error(self.y_train, y_train_pred),
                    'r2_score': r2_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'rmse': np.sqrt(mean_squared_error(self.y_test, y_test_pred)),
                    'mae': mean_absolute_error(self.y_test, y_test_pred),
                    'r2_score': r2_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        else:
            results = {
                'model_name': 'CatBoost Classifier',
                'train_metrics': {
                    'accuracy': accuracy_score(self.y_train, y_train_pred)
                },
                'test_metrics': {
                    'accuracy': accuracy_score(self.y_test, y_test_pred)
                },
                'feature_importance': dict(zip(self.X_train.columns, self.model.feature_importances_))
            }
        
        return results
    
    # ========== TIME SERIES MODELS ==========
    
    def train_arima(self, column: str, order: Tuple[int, int, int] = (1, 1, 1)) -> Dict:
        """
        Train an ARIMA model for time series forecasting.
        
        Args:
            column: Target column name
            order: ARIMA order (p, d, q)
            
        Returns:
            Dict: Model results and forecast
        """
        if not ARIMA_AVAILABLE:
            return {'error': 'ARIMA is not available. Install with: pip install statsmodels'}
        
        try:
            data = self.df[column].dropna()
            
            # Split data
            train_size = int(len(data) * 0.8)
            train_data = data[:train_size]
            test_data = data[train_size:]
            
            # Fit model
            model = ARIMA(train_data, order=order)
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=len(test_data))
            
            # Calculate metrics
            mse = mean_squared_error(test_data, forecast)
            mae = mean_absolute_error(test_data, forecast)
            
            return {
                'model_name': 'ARIMA',
                'order': order,
                'train_size': len(train_data),
                'test_size': len(test_data),
                'metrics': {
                    'mse': mse,
                    'rmse': np.sqrt(mse),
                    'mae': mae
                },
                'forecast': forecast.tolist(),
                'test_values': test_data.tolist(),
                'aic': fitted_model.aic,
                'bic': fitted_model.bic
            }
        except Exception as e:
            return {'error': str(e)}
    
    def train_prophet(self, date_column: str, target_column: str, 
                     periods: int = 30) -> Dict:
        """
        Train a Facebook Prophet model for time series forecasting.
        
        Args:
            date_column: Date column name
            target_column: Target column name
            periods: Number of periods to forecast
            
        Returns:
            Dict: Model results and forecast
        """
        if not PROPHET_AVAILABLE:
            return {'error': 'Prophet is not installed. Install with: pip install prophet'}
        
        try:
            # Prepare data
            df_prophet = self.df[[date_column, target_column]].copy()
            df_prophet.columns = ['ds', 'y']
            df_prophet = df_prophet.dropna()
            
            # Split data
            train_size = int(len(df_prophet) * 0.8)
            train_data = df_prophet[:train_size]
            test_data = df_prophet[train_size:]
            
            # Fit model
            model = Prophet()
            model.fit(train_data)
            
            # Make future dataframe
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            # Calculate metrics on test set
            test_forecast = forecast.iloc[train_size:train_size+len(test_data)]
            mse = mean_squared_error(test_data['y'], test_forecast['yhat'])
            mae = mean_absolute_error(test_data['y'], test_forecast['yhat'])
            
            return {
                'model_name': 'Prophet',
                'train_size': len(train_data),
                'test_size': len(test_data),
                'metrics': {
                    'mse': mse,
                    'rmse': np.sqrt(mse),
                    'mae': mae
                },
                'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records'),
                'periods': periods
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ========== HYPERPARAMETER TUNING ==========
    
    def tune_hyperparameters(self, model_name: str, param_grid: Dict, cv: int = 5) -> Dict:
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            model_name: Name of the model to tune
            param_grid: Dictionary of parameters to search
            cv: Number of cross-validation folds
            
        Returns:
            Dict: Best parameters and scores
        """
        # Define base models
        models = {
            'linear_regression': LinearRegression(),
            'ridge': Ridge(random_state=42),
            'lasso': Lasso(random_state=42),
            'decision_tree_reg': DecisionTreeRegressor(random_state=42),
            'decision_tree_clf': DecisionTreeClassifier(random_state=42),
            'random_forest_reg': RandomForestRegressor(random_state=42, n_jobs=-1),
            'random_forest_clf': RandomForestClassifier(random_state=42, n_jobs=-1),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000, n_jobs=-1),
            'svr': SVR(),
            'svc': SVC(random_state=42),
            'knn_reg': KNeighborsRegressor(n_jobs=-1),
            'knn_clf': KNeighborsClassifier(n_jobs=-1)
        }
        
        if model_name not in models:
            return {'error': f'Model {model_name} not supported for tuning'}
        
        model = models[model_name]
        
        # Perform grid search
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring='r2' if 'reg' in model_name or model_name in ['linear_regression', 'ridge', 'lasso', 'svr'] else 'accuracy',
            n_jobs=-1
        )
        
        grid_search.fit(self.X_train, self.y_train)
        
        return {
            'model_name': model_name,
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': {
                'mean_test_scores': grid_search.cv_results_['mean_test_score'].tolist(),
                'std_test_scores': grid_search.cv_results_['std_test_score'].tolist()
            }
        }
    
    @staticmethod
    def get_available_models() -> Dict[str, List[str]]:
        """
        Get list of available models.
        
        Returns:
            Dict: Available models by category
        """
        models = {
            'regression': [
                'Linear Regression',
                'Ridge Regression',
                'Lasso Regression',
                'Decision Tree',
                'Random Forest',
                'SVR (Support Vector Regression)',
                'KNN Regressor'
            ],
            'classification': [
                'Logistic Regression',
                'Decision Tree',
                'Random Forest',
                'SVC (Support Vector Classification)',
                'KNN Classifier'
            ],
            'gradient_boosting': [],
            'time_series': []
        }
        
        if XGBOOST_AVAILABLE:
            models['gradient_boosting'].append('XGBoost')
        
        if LIGHTGBM_AVAILABLE:
            models['gradient_boosting'].append('LightGBM')
        
        if CATBOOST_AVAILABLE:
            models['gradient_boosting'].append('CatBoost')
        
        if ARIMA_AVAILABLE:
            models['time_series'].append('ARIMA')
        
        if PROPHET_AVAILABLE:
            models['time_series'].append('Prophet')
        
        return models
