import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def main(n_samples: int = 100, seed: int = 42):
    rng = np.random.default_rng(seed=seed)
    
    # 1. X: 2D array (N, 1)
    X = rng.integers(low=5, high=121, size=(n_samples, 1)).astype(np.float64)
    
    print(f"X: {X}")
    # 2. noise: 1D array (N,)
    noise = rng.normal(loc=0.0, scale=1.0, size=n_samples)
    
    print(f"noise: {noise}")
    # 3. y: 1D array (N,)
    y = 200 + 12 * X[:, 0] + noise

    print(f"y: {y}")
    
    model = LinearRegression().fit(X, y)

    print(f"model coef_: {model.coef_[0]}")
    print(f"model intercept_: {model.intercept_}")

    y_predicted = model.predict(X)
    
    print(f"y_predicted: {y_predicted}")

    mae = mean_absolute_error(y, y_predicted)
    print(f"Mean Absolute Error: {mae}")

    print("\n[LƯU Ý KIẾN TRÚC]:")
    print("- Linear Regression dự đoán giá trị liên tục y ∈ (-∞, +∞) (phù hợp cho latency, cost, v.v.).")
    print("- KHÔNG dùng Linear Regression cho Intent Classification vì bài toán này cần xác suất rời rạc giữa các class.")


if __name__ == "__main__":
    main()
