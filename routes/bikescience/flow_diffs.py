import pandas as pd

from . import flow
from . import tiers
from . import arrow
from . import interface as interf

def get_flows(od_df, minimum=-1, maximum=-1, show=4, radius=1.0):
    '''
    Returns a the OD flows based on the given list of trips.
    
    Parameters
    od_df: origin-destination countings dataframe for the regions of the city, calculated by od_* functions in this module
    grid: a Grid object
    stations: a GeoDataframe with Point objects representing stations
    minimum: only draw arrows for the flows that are larger than this minimum number of trips
    maximum: only draw arrows for the flows that are smaller than this maximum number of trips
    show: a measure of the portion of flows to show. Typically between 2 and 5. 
    '''

    od_list = pd.DataFrame(columns=['origin_x','origin_y','destination_x','destination_y','weight','num_trips'])
    od_list.set_index
    
    # eliminate round-trips to the same station, which are not considering in this analysis
    filtered = od_df[(od_df['i_start'] != od_df['i_end']) | (od_df['j_start'] != od_df['j_end'])]

    if maximum == -1:
        maximum = filtered['trip counts'].max()
    if minimum == -1:
        minimum = maximum / show
        
    total_trips = filtered['trip counts'].sum()

    filtered = filtered[((filtered['trip counts'] >= minimum) & (filtered['trip counts'] <= maximum))]

    shown_trips = 0
    
    for idx, row in filtered.iterrows():
        num_trips = row['trip counts']
        
        shown_trips += num_trips
        weight = math.ceil( (num_trips-minimum)/maximum * 10)
        if weight == 0: weight = 1
        
        od_list.loc[idx] = [row['origin'].x,row['origin'].y,row['destination'].x,row['destination'].y,weight,shown_trips]

    return od_list


def diffs_map(start_trips, end_trips, grid, stations, stations_distances, perc_below):
    ## CHANGEE
    start_od = flow.od_countings(start_trips, grid, stations)
                                # station_index='id',
                                # start_station_index='index_start',
                                # end_station_index='index_end')
    start_gs = flow.grid_and_stations
    end_od = flow.od_countings(end_trips, grid, stations)
                                # start_station_index='index_start',
                                # end_station_index='index_end')
    end_gs = flow.grid_and_stations


    merge = start_od.merge(end_od, on=['i_start', 'j_start', 'i_end', 'j_end'], how='outer')

    print('merge')
    display(merge)

    # merge = start_od.merge(end_od, on=['i_start', 'j_start', 'i_end', 'j_end'], how='outer') \
    #         [['i_start', 'j_start', 'i_end', 'j_end',          # cell identifier
    #           'trip counts_x', 'origin_x', 'destination_x',    # first period
    #           'trip counts_y', 'origin_y', 'destination_y']]   # second period
    merge = merge[(merge['i_start'] != merge['i_end']) | (merge['j_start'] != merge['j_end'])]
    
    start_tiers, _ = tiers.find_tiers(start_od, start_trips, start_gs, stations_distances, max_tiers=4)
    start_top = start_tiers.loc[0]
    start_second = start_tiers.loc[1]
    start_how_many_below = (start_top['top'] - start_top['min']) * perc_below / 100.0
    # start_od = get_flows(start_od)
    # end_od = get_flows(end_od)

    end_tiers, _ = tiers.find_tiers(end_od, end_trips, end_gs, stations_distances, max_tiers=4)
    end_top = end_tiers.loc[0]
    end_second = end_tiers.loc[1]
    end_how_many_below = (end_top['top'] - end_top['min']) * perc_below / 100.0
    
    considering = merge[(merge['trip counts_x'] >= start_second['top'] - start_how_many_below) |
                        (merge['trip counts_y'] >= end_second['top'] - end_how_many_below)]
    
    fmap = grid.map_around(zoom=13)
    weight = 1
    for idx, row in considering.iterrows():
        if (not pd.isnull(row['trip counts_x'])) and (not pd.isnull(row['trip counts_y'])):
            start_in_4th = row['trip counts_x'] >= start_second['top']
            end_in_4th = row['trip counts_y'] >= end_second['top']
            if start_in_4th or end_in_4th:
                text = '{:.0f} trips before, {:.0f} trips after'.format(row['trip counts_x'], row['trip counts_y'])
                arrow.draw_arrow(fmap,
                                 row['origin_y'].y, row['origin_y'].x, row['destination_y'].y, row['destination_y'].x,
                                 text=text, weight=weight, color='blue', radius_fac=2.0)
        elif pd.isnull(row['trip counts_y']):
            if row['trip counts_x'] >= start_second['top']:
                text = '{:.0f} old trips'.format(row['trip counts_x'])
                arrow.draw_arrow(fmap,
                                 row['origin_x'].y, row['origin_x'].x, row['destination_x'].y, row['destination_x'].x,
                                 text=text, weight=weight, color='red', radius_fac=2.0)
        else:
            if row['trip counts_y'] >= end_second['top']:
                text = '{:.0f} new trips'.format(row['trip counts_y'])
                arrow.draw_arrow(fmap,
                                 row['origin_y'].y, row['origin_y'].x, row['destination_y'].y, row['destination_y'].x,
                                 text=text, weight=weight, color='green', radius_fac=2.0)
    return fmap