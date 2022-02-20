# Utilities for working with XG Boost
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from matplotlib import pyplot as plt
import json

# Plots useful things like the tree and importance for display
def plots(xgb_model, xgb_model_name, xgb_feat_map, xgb_plot):
    print("Plotting model quality data")
    try:
        bst = xgb.Booster()
        model = bst.load_model(xgb_model)
        model_name = xgb_model_name
        plt.rcParams["figure.figsize"]=[18,18]
        plt.rcParams["figure.autolayout"] = True
        num_trees = len(bst.get_dump(fmap=xgb_feat_map))
        print("Plotting trees: %s" % (num_trees-1))
        model_plot = plot_tree(bst, fmap=xgb_feat_map, num_trees=num_trees-1)
        model_plot.figure.savefig("%s/%s_tree.png" % (xgb_plot, model_name), dpi=300, rankdir='LR')
        print("Plotting feature importance")
        impt_plt = plot_importance(bst, fmap=xgb_feat_map)
        impt_plt.figure.savefig("%s/%s_importance.png" % (xgb_plot, model_name), dpi=300)
    except:
        print("Unable to plot our models")


# xgb_train_data is a string path to our training file
def train(xgb_train_data, num_rounds=50, xgb_conf=None ):
    params = {
        'max_depth': 50,
        'verbosity': 2,
        'learning_rate': 0.01,
        'objective': 'reg:logistic',        
    }

    dtrain = xgb.DMatrix(xgb_train_data)
    bst = xgb.train(params=params, dtrain=dtrain, num_boost_round=1000)

    if xgb_conf is not None:
        with open(xgb_conf) as json_file:
            params = json.load(json_file)
    print("Training XG Boost on %s for %s rounds with params: %s" % (xgb_train_data, num_rounds, params))
    #print("IMPLEMENT ME: train()")
    return bst, params

