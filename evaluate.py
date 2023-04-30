def plot_residuals(y, yhat):
    return 0

def regression_errors(y, yhat): 
    return sse, ess, tss, mse, rmse

def baseline_mean_errors(y):
    return sse_base, mse_base, rmse_base

def better_than_baseline(y, yhat): 
    if [model] > [baseline_model]:
        return true
    else:
        return false