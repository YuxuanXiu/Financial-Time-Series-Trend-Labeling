import akshare as ak
from trend_labeling import auto_labeling
import matplotlib.pyplot as plt


def plot_ts_with_trend_and_financial_extremes(ax, Date_list, Cls_list, trend_labels, x_interval):
    x = [i for i in range(len(Date_list))]
    for i in range(len(trend_labels) - 1):
        j = i
        while j < len(trend_labels) - 2 and trend_labels[j] == trend_labels[j + 1]:
            j = j + 1
        if trend_labels[j - 1] == -1:
            color = 'orange'
        elif trend_labels[j - 1] == 1:
            color = 'skyblue'
        else:
            color = 'white'
        ax.plot(x[i:j+1], Cls_list[i:j+1], color)
    ax.set_xlabel('Date')
    ax.set_ylabel("Price")
    x_sampled = []
    for i in x:
        if i % x_interval == 0:
            x_sampled.append(i)
    x = x_sampled
    xtick = [Date_list[i] for i in x]
    ax.set_xticks(x)
    ax.set_xticklabels(xtick)
    for xtick in ax.get_xticklabels():
        xtick.set_rotation(0)
    return ax

if __name__ == "__main__":
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399300")
    stock_zh_index_daily_df['date'] = stock_zh_index_daily_df['date'].astype(str)
    stock_zh_index_daily_df = stock_zh_index_daily_df[stock_zh_index_daily_df['date'] >= '2005-04-08']
    Date_list = stock_zh_index_daily_df['date'].values.tolist()
    Cls_list = stock_zh_index_daily_df['close'].values.tolist()
    for w in [0.1, 0.15, 0.2]:
        trend_labels, _ = auto_labeling(Cls_list, Date_list, w)
        fig = plt.figure(figsize=(15, 5), dpi=300)
        ax = plt.gca()
        ax = plot_ts_with_trend_and_financial_extremes(ax, Date_list, Cls_list, trend_labels, x_interval=300)
        title = "Trend Labeling of CSI 300 with w={}%".format(w*100)
        ax.set_title(title)
        plt.savefig('figures/' + '{}.png'.format(title))
