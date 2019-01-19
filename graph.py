def leaflet(fname):
    """
    Load a gps file and show the track on map with mapleaflet
    """
    # global uuid_to_file
    # print uuid_to_file
    # gpx_file = uuid_to_file[uuid]
    gpx = gpxpy.parse(open(fname, 'r'))
    lat = []
    lon = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    # Plot the path as red dots connected by a blue line
    # plt.hold(True)
    # plt.plot(lon, lat, 'r.')
    plt.plot(lon, lat, 'b')
    #
    # Create the map. Save the file to basic_plot.html. _
    # map.html is the  default
    # root, ext = os.path.splitext(__file__)
    # mapfile = 'skeleton/'+root + '.html'
    mapfile = 'skeleton/parser.html'
    #
    # if 'path' is not specified
    #
    mplleaflet.save_html(fileobj=mapfile)
    print("Generating mplleaflet map")
    return 

def graphs(data):
    """
    Print the graph of all years using pygal
    Return a list of svg rendered graph
    """
    line_chart = pygal.Line(
        x_label_rotation=30, x_labels_major_count=12, interpolate='cubic')
    bar_chart = pygal.Bar(x_label_rotation=30, x_labels_major_count=12)
    box_chart = pygal.Box(x_label_rotation=30, x_labels_major_count=12)
    data_grouped_year = data.groupby(['Year'])

    for year, datagr in data_grouped_year:
        datagr_m = datagr.groupby(['Month'])

        bar_chart.title = 'Km by month by year'
        bar_chart.x_labels = [i for i, j in datagr_m]
        bar_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    zip(
                                    datagr_m['Length'].sum(),
                                    datagr_m['Length'].mean()
                                    )])

        box_chart.title = 'Km by month by year'
        box_chart.x_labels = [i for i, j in datagr_m]
        box_chart.add('%s' % year, [{'value': i,
                                     'label': 'moy/act:%s' % str(j)}
                                    for i, j in
                                    zip(
                                    datagr_m['Length'].sum(),
                                    datagr_m['Length'].mean()
                                    )])

        line_chart.title = 'Km by month by year'
        line_chart.x_labels = range(1, 13)
        line_chart.add('%s' % year, datagr_m['Length'].sum().cumsum())
    # bar_chart.render_to_file('./testbar.svg')
    # box_chart.render_to_file('./testbox.svg')
    # line_chart.render_to_file('./testline.svg')
    figs = [line_chart.render_data_uri(), 
            bar_chart.render_data_uri(),]
            # box_chart.render_data_uri()]
    return figs

def termgraphRun(dataF):
    """
    Graph in term
    """
    args = {'filename': './test_termgraph.txt', 
            'title': None, 
            'width': 50, 
            'format': '{:<5.2f}', 
            'suffix': '', 
            'no_labels': False, 
            'color': None, 
            'vertical': False, 
            'stacked': False, 
            'different_scale': False, 
            'calendar': True, 
            'start_dt': None, 
            'custom_tick': '', 
            'delim': '', 
            'verbose': False, 
            'version': False}

    data   = [[i] for i in dataF['Length'].tolist()]
    labels = (dataF['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))).tolist()
    args1 = args
    args1['start_dt'] = '2018-01-01'

    sys.stdout.write('\n')
    sys.stdout.write('########### GRAPHS\n')
    sys.stdout.write('\n')

    tgraph.calendar_heatmap(data, labels, args1)

    datay  = dataF[dataF.Year == 2018].groupby(['Month'])
    # print(datay.loc['Length'].sum())
    labels = []
    data   = []
    for key, item in datay:
        # print(datay.get_group(key), "\n\n")
        labels.append(month_name[key][:3])
        data.append([datay.get_group(key)['Length'].sum()])

    sys.stdout.write('\n')
    sys.stdout.write('\n')

    tgraph.chart(None, data, args, labels)

    sys.stdout.write('\n')
    sys.stdout.write('########### TOTAL\n')
    sys.stdout.write('\n')

    ystats = yearStats(dataF)
    #(km_y, activities_y, km_t, day_and_km)
    print('Kilometrage    : %s'%ystats[0])
    print('Nombre sorties : %s'%ystats[1])
    sys.stdout.write('\n')
    return