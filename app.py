from cProfile import label
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
colors = {
    'grey': '#4C566A',
    'black': '#2E3440',
    'white': '#D8DEE9',
    'dark-blue': '#5E81AC',
    'red': '#BF616A',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'orange': '#D08770',
    'purple': '#B48EAD',
    'light-blue': '#8FBCBB'
}
#url = "https://www.dropbox.com/s/xonh8avcmutamw3/diem_clean_with_0_with_rank.csv?dl=1"
#url = "https://drive.google.com/uc?id=" + url.split('/')[-2]
url = "diem_clean_with_0_with_rank.csv"
df = pd.read_csv(url, dtype={'F_MAMH': str, "NHHK": "str", "F_TENMHVN": "str"})
majors = df.F_TENNGVN.drop_duplicates()
subjects = df.F_TENMHVN.drop_duplicates()
semesters = ["All semesters", "151", "152", "153", "161", "162", "163", "171", "172"]
semesters_without_all = ["151", "152", "153", "161", "162", "163", "171", "172"]
list_type = ["TILEBT", "TILETN", "TILEBTLDA", "TILEKT", "TILETHI"]
cluster_features = ["MASV1","BT", "BTLDA", "TN", "KT", "THI", "TKET", "TKET_RANK"]
global_labels = {
    "TILEBT": "Percentage of Exercise",
    "TILETN": "Percentage of Lab",
    "TILEBTLDA": "Percentage of Assignment",
    "TILEKT": "Percentage of Midterm",
    "TILETHI": "Percentage of Final",
    "BT": "Exercise",
    "TN": "Lab",
    "BTLDA": "Assignment",
    "KT": "Midterm",
    "THI": "Final",
    "F_TENMHVN": "Subject",
    "F_TENNGVN": "Major",
    "NHHK": "Semester",
    "TKET": "Grade"

}
studentAllSemHover = {
    'TKET': True,
    'NHHK': True,
    'F_TENMHVN': False
}
studentOneSemHover = {
    'F_TENMHVN': False,
    'BT': True,
    'TN': True,
    'BTLDA': True,
    'KT': True,
    'THI': True,
    'TKET': True,
}
app = Dash(__name__)
server = app.server
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(
    children= [
        html.Div(
            children=[
                html.H1(
                    children='HCMUT Student Score Dashboard',
                    style={
                        'textAlign': 'center',
                        #'background': colors["yellow"]
                    }
                )
            ]
        ),
        html.Div(
            children=[
                html.H2(
                    children='Visualize student results',
                    style={
                        'textAlign': 'center',
                        #'background': colors["yellow"]
                    }
                )
            ]
        ),
        
        dcc.Tabs([
            dcc.Tab(label= 'School overview', children=[
            html.H3(
                children='Grade overview',
            ),
            html.Div(
                children= [
                html.Div(
                    children=[
                        html.Label('Choose the major:'),
                        dcc.Dropdown(majors, value="Điện - Điện tử", id="major-for-teacher"),
                    ], 
                    style={'padding': 10, 'flex': 1}),

                html.Div(
                    children=[
                        html.Label('Choose the subject:'),
                        dcc.Dropdown(subjects, value="Những NgLý cơbản CN M-Lê", id="subject-for-teacher"),
                    ], 
                    style={'padding': 10, 'flex': 1}),
                html.Div(
                    children=[
                        html.Label('Choose the semester:'),
                        dcc.Dropdown(semesters, value="All semesters", id="semester-for-teacher"),
                    ],
                    style={'padding': 10, 'flex': 1})
                ], 
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
            html.Div(
                children=[
                    dcc.Graph(id='histogram-for-teacher'),
                    dcc.Graph(id='subject-score-distribution')
                ],
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
            html.Hr(),
            html.H3(
                children='Grade comparison'
            ),
            html.Div(
                children= [
                    html.Div(
                    children=[
                        html.Label('Choose the majors that you want to compare:'),
                        dcc.Dropdown(majors, value=["Điện - Điện tử", "Cơ khí-Cơ điện tử"], multi=True, id="majors-compare-major"),
                    ], 
                    style={'padding': 10, 'flex': 1}),

                html.Div(
                    children=[
                        html.Label('Choose the subject that you want to compare:'),
                        dcc.Dropdown(subjects, value="Anh văn 1", id= "majors-compare-subject"),
                    ], 
                    style={'padding': 10, 'flex': 1}),
                html.Div(
                    children=[
                        html.Label('Choose the semester:'),
                        dcc.Dropdown(semesters_without_all, value="151", id="majors-compare-semester"),
                    ],
                    style={'padding': 10, 'flex': 1})
                ], 
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
            html.Div(
                children=[
                    dcc.Graph(id='majors-compare-graph')
                ]
            ),
            html.Hr(),
            html.H3(
                children='Grade trend'
            ),
            html.Div(
                children= [
                    html.Div(
                    children=[
                        html.Label('Choose the major that you want to see:'),
                        dcc.Dropdown(majors, value="Cơ khí-Cơ điện tử", id="subject-trend-major"),
                    ], 
                    style={'padding': 10, 'flex': 1}),

                html.Div(
                    children=[
                        html.Label('Choose the subject that you want to see:'),
                        dcc.Dropdown(subjects, value="Anh văn 1", id= "subject-trend-subject"),
                    ], 
                    style={'padding': 10, 'flex': 1})
                ], 
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
            html.Div(
                children=[
                    dcc.Graph(id='subject-trend-graph')
                ]
            ),
            html.Hr(),
            html.H3(
                children="Grade clustering"
            ),
            html.Div(
                children=[
                    html.Div(
                    children=[
                        html.Label('Choose the major that you want to see:'),
                        dcc.Dropdown(majors, value="Cơ khí-Cơ điện tử", id="grade-cluster-major"),
                    ], 
                    style={'padding': 10, 'flex': 1}),

                    html.Div(
                    children=[
                        html.Label('Choose the subject that you want to see:'),
                        dcc.Dropdown(subjects, value="Anh văn 1", id="grade-cluster-subject"),
                    ], 
                    style={'padding': 10, 'flex': 1}),
                    html.Div(
                    children=[
                        html.Label('Choose the semester:'),
                        dcc.Dropdown(semesters_without_all, value="151", id="grade-cluster-semester"),
                    ],
                    style={'padding': 10, 'flex': 1})
                ],
                style={'display': 'flex', 'flex-direction': 'row'}
            ),
            html.Div(
                children=[
                    dcc.Graph(id='grade-cluster-graph-tsne')
                ]
            ),
            html.Hr(),
        ]
    ),
        dcc.Tab(label= 'Student overview', children=[
            html.Div(
                    children= [
                        html.Div(
                            children=[
                                html.Label('Type the Student ID: '),
                                html.Br(),
                                dcc.Input(id= "student_id", value='36150879', type='text', style={'width': '99%', 'height': '30px'}),
                            ], 
                            style={'padding': 10, 'flex': 1}
                            ),
                        html.Div(
                            children=[
                                html.Label('Choose the semester:'),
                                dcc.Dropdown(id='student-semester',options=semesters, value='All semesters'),
                            ], 
                            style={'padding': 10, 'flex': 1}),
                        html.Br(),
                        ],
                    style={'display': 'flex', 'flex-direction': 'row'}
                ),
            html.Div(
                    children=[
                        dcc.Graph(id="student-history")
                    ]
                )
        ])
    ])
        
    ]
)

@app.callback(
    Output(component_id='student-history', component_property='figure'),
    Input(component_id='student_id', component_property='value'),
    Input(component_id='student-semester', component_property='value')
)
def student_history_graph(student_id, student_semester):
    student_df = df[df.MASV1 == int(student_id)]
    if student_semester == "All semesters":
        fig = px.bar(student_df, y='TKET', x='F_TENMHVN', text = "NHHK", color = "NHHK", hover_data=studentAllSemHover, labels=global_labels)
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.update_layout(hovermode="x")
        fig.add_hline(y=5, line_dash = "dot", annotation_text="Passing grade")
        fig.update_layout(transition_duration=500)
        fig.add_hline(y=5, line_dash = "dot") 
    else:
        student_df = student_df[student_df.NHHK == student_semester]
        fig = px.bar(data_frame=student_df, y='TKET', x='F_TENMHVN', text = "TKET", color = "F_TENMHVN", hover_data=studentOneSemHover, labels=global_labels)
        fig.update_yaxes(range=[0, 10])
        fig.add_hline(y=5, line_dash = "dot", annotation_text="Passing grade")
        fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output(component_id='histogram-for-teacher', component_property='figure'),
    Input(component_id='major-for-teacher', component_property='value'),
    Input(component_id='subject-for-teacher', component_property='value'),
    Input(component_id='semester-for-teacher', component_property='value')
)
def subject_histogram(major, subject, semester):
    filtered_df = df[(df.F_TENNGVN == major) & (df.F_TENMHVN == subject)]
    if semester == "All semesters":
        chart_title = "Grade histogram of " + subject + " in " + major
        fig = px.histogram(filtered_df, x="TKET", color="NHHK", range_x=[0, 10], nbins=20, title=chart_title, labels=global_labels)
        # add a dot line to show the passing grade is 5
        fig.update_layout(transition_duration=500)
    else:
        chart_title = "Grade histogram of " + subject + " in " + major + " in semester " + semester
        one_sem_filtered_df = filtered_df[filtered_df.NHHK == semester]
        fig = px.histogram(one_sem_filtered_df, x="TKET", range_x=[0, 10], nbins=20, title=chart_title, labels=global_labels, marginal="violin")
        fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output(component_id='subject-score-distribution', component_property='figure'),
    Input(component_id='subject-for-teacher', component_property='value'),
    Input(component_id='semester-for-teacher', component_property='value')
)
def subject_score_distribution(subject, semester):    # , semester):
    filtered_df = df[df.F_TENMHVN == subject]
    if semester == "All semesters":
        each_sem_df = filtered_df.groupby('NHHK', as_index=False).first()
        chart_title = "Grade distribution of " + subject
        fig = px.bar(each_sem_df, x="NHHK", y=["TILEBT", "TILETN", "TILEBTLDA", "TILEKT", "TILETHI"],
        title=chart_title, labels= global_labels)
        return fig

    else:
        one_sem_filtered_df = filtered_df[filtered_df.NHHK == semester].iloc[1]
        tmp_data = list()
        for type in list_type:
            if one_sem_filtered_df[type] != 0:
                tmp_data.append([type, one_sem_filtered_df[type]])
        tmp_df = pd.DataFrame(tmp_data, columns = ["Type", "Percentage"])
        chart_title = "Grade distribution of " + subject + " in " + semester
        fig = px.pie(data_frame=tmp_df, values="Percentage", names="Type", title=chart_title, labels= global_labels)
        fig.update_layout(transition_duration=500)
        return fig

@app.callback(
    Output(component_id='majors-compare-graph', component_property='figure'),
    Input(component_id='majors-compare-major', component_property='value'),
    Input(component_id='majors-compare-subject', component_property='value'),
    Input(component_id='majors-compare-semester', component_property='value')
)
def majors_subject_score_comparator(majors, subject, semester):
    filtered_df = df[(df.F_TENMHVN == subject) & (df.NHHK == semester) & (df.F_TENNGVN.isin(majors))]
    fig = px.box(filtered_df, y='TKET', x='F_TENNGVN', color = "F_TENNGVN", title= "Subject grade comparison",labels=global_labels, 
    points= "all")
    return fig


@app.callback(
    Output(component_id='subject-trend-graph', component_property='figure'),
    Input(component_id='subject-trend-major', component_property='value'),
    Input(component_id='subject-trend-subject', component_property='value'),
)
def subject_trend_graph(major, subject):
    filtered_df = df[(df.F_TENMHVN == subject) & (df.F_TENNGVN == major)]
    fig = px.box(filtered_df, y='TKET', x='NHHK', color = "NHHK", title= "Subject trend",labels=global_labels,points="all")
    #fig = px.line(filtered_df, x="NHHK", y="TKET", color="F_TENMHVN", title="Subject trend", labels=global_labels)
    return fig

@app.callback(
    Output(component_id='grade-cluster-graph-tsne', component_property='figure'),
    Input(component_id='grade-cluster-major', component_property='value'),
    Input(component_id='grade-cluster-subject', component_property='value'),
    Input(component_id='grade-cluster-semester', component_property='value')
)
def grade_cluster_graph(major, subject, semester):
    filtered_df = df[(df.F_TENMHVN == subject) & (df.F_TENNGVN == major) & (df.NHHK == semester)][cluster_features]
    filtered_df = filtered_df[filtered_df != 13].dropna()
    df_masv = filtered_df["MASV1"]
    df_label = filtered_df["TKET_RANK"]
    filtered_df = filtered_df.drop(columns=["MASV1", "TKET_RANK"])
    # triple the TkET score to make it more visible
    filtered_df["TKET"] = filtered_df["TKET"] * 4
    df_masv.reset_index(drop=True, inplace=True)
    df_label.reset_index(drop=True, inplace=True)
    filtered_df.reset_index(drop=True, inplace=True)
    tsne= TSNE(n_components=2, random_state=0, learning_rate="auto", perplexity=10, init="random")
    transform_df_tsne= tsne.fit_transform(filtered_df)
    transform_df_tsne= pd.concat([pd.DataFrame(data=transform_df_tsne, columns=["x", "y"]), df_label, filtered_df, df_masv], axis=1)
    # Reverse the TkET score
    transform_df_tsne["TKET"] = transform_df_tsne["TKET"] / 4
    fig = px.scatter(transform_df_tsne, x="x", y="y", color=df_label, hover_data={"x": False, "y": False, "TKET_RANK": False, "BT": True,
"BTLDA": True, "TN": True, "KT": True, "THI": True, "MASV1": True, "TKET": True} )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)