import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import seaborn as sns

outfit_bold_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Outfit-Bold.ttf"
outfit_thin_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Outfit-VariableFont_wght.ttf"
cabin_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Cabin[wdth,wght].ttf"


outfit_bold = font_manager.FontProperties(fname=outfit_bold_path)
outfit_thin = font_manager.FontProperties(fname=outfit_thin_path)
cabin = font_manager.FontProperties(fname=cabin_path)


def pie_chart(df):

    data = df["category"].value_counts().to_dict()
    sorted_data = sorted(data.items(), key=lambda kv: kv[1], reverse=True)

    x = [val for _, val in sorted_data]
    labels = [key for key, _ in sorted_data]
    colors = ["#bde0fe", "#a2d2ff", "#ffc8dd"]

    total = sum(x)
    percentages = ["{0:.1%}".format(value / total) for value in x]

    fig, ax = plt.subplots(figsize=(14, 6), dpi=150)
    fig.subplots_adjust(top=0.80, bottom=0.1)

    # Move pie chart to the right
    ax.set_position([0.4, 0.3, 0.5, 0.5])

    # Pie chart
    wedges, texts = ax.pie(
        x,
        labels=percentages,
        startangle=90,
        counterclock=False,
        colors=colors,
        textprops={"ha": "center", "fontsize": 12, "fontproperties": cabin},
        labeldistance=1.2,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )

    # Legend
    ax.legend(
        labels=labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        title="Category",
        title_fontproperties=cabin,
        prop=cabin,
    )

    # Title
    fig.suptitle(
        "Breakdown of Transaction Categories",
        fontsize=18,
        fontproperties=outfit_bold,
        x=0.05,
        y=0.95,
        ha="left",
    )

    # Subtitle — independent of pie chart
    fig.text(
        0.05,
        0.85,  # x (left), y (height below title)
        "Each slice represents the proportion of a specific transaction type.\n"
        "Normal, Anomalous, or Fraudulent - within the entire dataset.",
        fontsize=12,
        fontproperties=outfit_thin,
        color="black",
        ha="left",
    )

    os.makedirs("images", exist_ok=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.subplots_adjust(top=0.85)

    image_path = os.path.join("images", "pie_chart.svg")
    plt.savefig(image_path, format="svg")
    plt.close()


def box_plot(df):
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.boxplot(
        [
            df[df["category"] == category]["num_of_unique_IPs_used"]
            for category in df["category"].unique()
        ],
        vert=False,
    )

    # Set the y-axis labels to the categories
    ax.set_yticks(range(1, len(df["category"].unique()) + 1))
    ax.set_yticklabels(df["category"].unique())

    # Title
    fig.suptitle(
        "Distribution of Unique IPs Used in All Categories",
        fontsize=18,
        fontproperties=outfit_bold,
        x=0.05,
        y=1.06,
        ha="left",
    )

    # subtitle
    fig.text(
        -0.09,
        1.1,
        "This box plot shows the distribution of the number of unique IPs used by users in different categories of transactions. "
        "\nThe spread of the data is visualized with quartiles, while outliers are marked separately.",
        fontsize=12,
        fontproperties=outfit_thin,
        color="black",
        ha="left",
        va="center",
        transform=plt.gca().transAxes,
    )

    ax.set_xlabel(
        "Number of Unique IPs Used",
        fontsize=12,
        fontproperties=cabin,
        color="gray",
        labelpad=20,
    )
    ax.set_ylabel(
        "Transaction Category",
        fontsize=12,
        fontproperties=cabin,
        color="gray",
        labelpad=20,
    )
    os.makedirs("images", exist_ok=True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.subplots_adjust(top=0.85)
    image_path = os.path.join("images", "ip_box_plot.svg")
    plt.savefig(image_path, format="svg")
    plt.close()
