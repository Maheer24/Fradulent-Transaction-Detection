import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import plotly.express as px
import os
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

# C:\Users\HP>pip install kaleido==0.1.0.post1

outfit_bold_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Outfit-Bold.ttf"
outfit_thin_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Outfit-VariableFont_wght.ttf"
cabin_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Cabin[wdth,wght].ttf"
outfit_extra_bold_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\Outfit-ExtraBold.ttf"
open_sans_reg_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\frontend\src\assets\OpenSans-Regular.ttf"

open_sans_reg = font_manager.FontProperties(fname=open_sans_reg_path)
outfit_bold = font_manager.FontProperties(fname=outfit_bold_path)
outfit_thin = font_manager.FontProperties(fname=outfit_thin_path)
cabin = font_manager.FontProperties(fname=cabin_path)
outfit_extra_bold = font_manager.FontProperties(fname=outfit_extra_bold_path)


def pie_chart(df):

    data = df["status"].value_counts().to_dict()
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


def cases_by_location(df):
    print("Creating bar chart...")
    counts = df.groupby(["location", "status"]).size().reset_index(name="count")
    print("Define custom colours")
    # Custom color map
    custom_colors = {
        "Fraudulent": "#ffc8dd",
        "Normal": "#bde0fe",
        "Anomalous": "#ffedf4",
    }

    # Plot
    print("Creating plot")
    fig = px.bar(
        counts,
        x="location",
        y="count",
        width=1200,
        height=500,
        color="status",
        color_discrete_map=custom_colors,
        title="📍 Status Distribution by Location",
        labels={
            "location": "City",
            "count": "Number of Cases",
            "status": "Transaction Status",
        },
    )

    # Add custom layout with merged annotations
    print("Adding custom layout with merged annotations")
    fig.update_layout(
        title={
            "text": "📍<b>Status Distribution by Location</b><br>",
            "x": 0.5,
            "xanchor": "center",
        },
        title_font=dict(family=outfit_extra_bold.get_name(), size=40, color="black"),
        legend_title_text="Transaction Status",
        margin=dict(t=100, b=100),
        annotations=[
            dict(
                text="This chart shows how many 'Normal', 'Fraudulent', and 'Anomalous' transactions occurred in each city.",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.1,  # Position just below the main title
                xanchor="center",
                font=dict(size=16, color="black"),
            ),
            dict(
                text="ℹ️ Use this chart to understand which locations have more suspicious activity.",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.25,
                font=dict(size=12),
                align="left",
                bgcolor="#f8f9fa",
                opacity=0.8,
            ),
        ],
    )
    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", "location_bar_chart.svg")
    fig.write_image(image_path, format="svg")


def unique_ips_by_category(data):
    fig = px.bar(
        data_frame=data,
        width=1450,
        height=600,
        x="status",
        y="num_of_unique_IPs_used",
        color="status",
        labels={
            "num_of_unique_IPs_used": "Number of Unique IPs",
            "status": "Transaction Status",
        },
        color_discrete_sequence=["#bde0fe", "#fb6f92", "#fdffb6"],
        category_orders={"status": ["Normal", "Fraudulent", "Anomalous"]},
    )

    fig.update_layout(
        title={
            "text": "<b>Number of Unique IPs Used by Transaction Status</b>",
            "x": 0.68,
            "xanchor": "right",
        },
        title_font=dict(family=outfit_extra_bold.get_name(), size=40, color="#3b3b3b"),
        xaxis_title="Transaction Status",
        yaxis_title="Number of Unique IPs",
        bargap=0.2,
        legend_title_text="Transaction Status",
        margin=dict(t=120, b=80),  # More space at top and bottom
        annotations=[
            dict(
                text="🔍 This chart shows how many unique IP addresses were used for each transaction status. A higher number of IPs may indicate suspicious activity.",
                x=1.03,
                y=1.1,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=18, color="gray", family=open_sans_reg.get_name()),
                align="right",
            )
        ],
    )

    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", "unique_ip_bar_chart.svg")
    fig.write_image(image_path, format="svg")


def wallet_balance_account_age_bubble_chart(data):
    fig = px.scatter(
        data_frame=data,
        x="account_age_days",
        y="wallet_balance",
        size="login_count",  # Bubble size based on login count
        color="status",
        hover_name="location",
        size_max=70,  # Slightly increased max bubble size
        color_discrete_sequence=["#fb6f92", "#bde0fe", "#fdffb6"],
        labels={
            "account_age_days": "Account Age (days)",
            "wallet_balance": "Wallet Balance (USD)",
            "status": "Transaction Status",
        },
    )

    fig.update_layout(
        title={
            "text": "<b>Wallet Balance vs Account Age",
            # <br>(Bubble Size = Login Count)</b>
            "x": 0.42,
            "xanchor": "right",
        },
        title_font=dict(family=outfit_extra_bold.get_name(), size=38, color="#3b3b3b"),
        xaxis_title="<b>Account Age (days)</b>",
        yaxis_title="<b>Wallet Balance (USD)</b>",
        height=650,
        width=1420,
        margin=dict(t=150, b=100),
        legend_title_text="<b>Transaction Status</b>",
        annotations=[
            dict(
                text=(
                    "This chart visualizes how account age and wallet balance relate across different transaction types. Each bubble represents a user. Larger bubbles indicate higher login activity.<br>"
                    "Clusters of large bubbles with young account ages and high balances may hint at suspicious behavior."
                ),
                x=1.1,
                y=1.15,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16, color="gray", family=open_sans_reg.get_name()),
                align="left",
            )
        ],
    )
    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", "wallet_bal_acc_age_bubble_chart.svg")
    fig.write_image(image_path, format="svg")


def deposit_status_pie_chart(data):
    fig = px.pie(
        data,
        width=1200,
        height=600,
        names="deposit_status",
        title="🏦 Distribution of Deposit Status Across Transaction Types",
        hole=0.4,
        facet_col="status",  # Create separate pie charts for each transaction status
        color_discrete_sequence=[
            "#bde0fe",
            "#fb6f92",
            "#fdffb6",
        ],  # Custom color scheme
    )

    # Display both label and percentage inside slices
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=14, color="black"),
        pull=[0.02]
        * len(
            data["deposit_status"].unique()
        ),  # Slightly pull slices for better visibility
    )
    fig.for_each_annotation(
        lambda a: a.update(
            text=a.text.split("=")[-1].strip(), font=dict(size=18, color="#3b3b3b")
        )
    )

    # Layout enhancements
    fig.update_layout(
        title={
            "text": "<b>Deposit Status Breakdown by Transaction Status</b>",
            "x": 0.01,
            "xanchor": "left",
        },
        title_font=dict(family=outfit_extra_bold.get_name(), size=32, color="#3b3b3b"),
        legend_title_text="<b>Deposit Status</b>",
        margin=dict(t=100, b=80),
    )

    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", "deposit_status_pie_chart.svg")
    fig.write_image(image_path, format="svg")


def radar_chart_transaction_profiles(df):

    # 1. Select relevant features
    features = [
        "num_of_unique_IPs_used",
        "login_count",
        "num_of_frequent_operations",
        "c2c_place_order_count",
        "c2c_release_order_count",
        "gift_card_created_amount",
        "gift_card_redeemed_amount",
        "amount",
        "wallet_balance",
        "wallet_free_balance",
        "wallet_locked_balance",
        "account_age_days",
    ]

    # 2. Compute mean values for each transaction status group
    grouped = (
        df[df["status"].isin(["Normal", "Fraudulent", "Anomalous"])]
        .groupby("status")[features]
        .mean()
    )

    # 3. Normalize the values using MinMaxScaler for consistent scale
    scaler = MinMaxScaler()
    normalized = pd.DataFrame(
        scaler.fit_transform(grouped), columns=features, index=grouped.index
    )

    # 4. Prepare data for radar chart (loop back to the first feature for full circle)
    categories = features + [features[0]]
    normal_values = normalized.loc["Normal"].tolist() + [
        normalized.loc["Normal"].tolist()[0]
    ]
    anomalous_values = normalized.loc["Anomalous"].tolist() + [
        normalized.loc["Anomalous"].tolist()[0]
    ]
    fraud_values = normalized.loc["Fraudulent"].tolist() + [
        normalized.loc["Fraudulent"].tolist()[0]
    ]

    # 5. Create radar chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=normal_values,
            theta=categories,
            fill="toself",
            name="Normal",
            line_color="green",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=anomalous_values,
            theta=categories,
            fill="toself",
            name="Anomalous",
            line_color="orange",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=fraud_values,
            theta=categories,
            fill="toself",
            name="Fraudulent",
            line_color="red",
        )
    )

    fig.update_layout(
        width=1200,
        height=700,
        title={
            "text": "<b>Comparison of User Behavior Across Transaction Types</b><br>",
            "x": 0.03,
            "y": 0.95,
            "xanchor": "left",
        },
        title_font=dict(family=outfit_bold.get_name(), size=30, color="#222"),
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 1], tickfont=dict(size=12)  # Normalized range
            ),
            angularaxis=dict(tickfont=dict(size=12)),
        ),
        legend_title_text="<b>Transaction Status</b>",
        # height=700,
        margin=dict(t=150, b=80),
        annotations=[
            dict(
                text="This radar chart compares average user behavior for different transaction types (Normal, Anomalous, Fraudulent). The features show key activity metrics like</sup><br>"
                "account age, wallet balance, login frequency, and gift card usage.",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=-0.03,
                y=1.22,  # Position just below the main title
                xanchor="left",
                font=dict(size=16, color="black"),
            ),
            dict(
                text="This chart shows the relative behavior of users based on various features (e.g., wallet balance, login count, gift card usage). Features are normalized for easy comparison.",
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.12,
                showarrow=False,
                font=dict(size=14, color="gray"),
                align="center",
            ),
        ],
    )
    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", "profile_radar_chart.svg")
    fig.write_image(image_path, format="svg")


def box_plot(df):
    fig, ax = plt.subplots(figsize=(7, 4))

    ax.boxplot(
        [
            df[df["status"] == category]["num_of_unique_IPs_used"]
            for category in df["status"].unique()
        ],
        vert=False,
    )

    # Set the y-axis labels to the categories
    ax.set_yticks(range(1, len(df["status"].unique()) + 1))
    ax.set_yticklabels(df["status"].unique())

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
