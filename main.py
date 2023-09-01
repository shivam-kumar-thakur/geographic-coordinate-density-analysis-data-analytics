# Function to calculate the haversine distance between two coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance in kilometers
    distance = R * c
    return distance


# Function to find the number of points within a certain distance for all unique coordinates
def specific_co_ordintes(list_of_unique_coordinates, distance_circle_in_km):
    store_each_coordinta_count = []  # [[lat, long], total_count_inside_given_distance, avg_speed]

    # Loop through each unique coordinate
    for i in range(len(list_of_unique_coordinates)):
        lat1, lon1, speed1 = list_of_unique_coordinates[i]
        count = 0
        speed_total = 0

        # Compare with other unique coordinates
        for j in range(len(list_of_unique_coordinates)):
            if i != j:  # Avoid comparing the same coordinates
                lat2, lon2, speed2 = list_of_unique_coordinates[j]

                # Check if the haversine distance is within the given circle distance
                if haversine_distance(lat1, lon1, lat2, lon2) <= distance_circle_in_km:
                    count = count + 1
                    speed_total = speed_total + speed2

        # Calculate average speed and store information
        avg_speed = speed_total / count if count > 0 else 0  # Handle divide by zero
        store_each_coordinta_count.append([[lat1, lon1], count, round(avg_speed)])

    return store_each_coordinta_count


# Function to sort coordinates based on certain criteria and remove overlapping points
def specific_points(co_ordinates_count, reverse_value, sort_on_basis, circle_radius_in_km):
    # Sort coordinates based on criteria
    sorted_co_ordinates = sorted(co_ordinates_count, key=lambda x: x[sort_on_basis], reverse=reverse_value)
    final_specific_points = [sorted_co_ordinates[0]]  # Store the first element

    for i in range(1, len(sorted_co_ordinates)):
        store_data2 = sorted_co_ordinates[i]
        lat2, lon2 = store_data2[0]

        # Check if the distance between two points is greater than circle_radius_in_km for all know points
        flag=True
        for j in final_specific_points:
            lat1, lon1 = j[0]
            if (haversine_distance(lat1, lon1, lat2, lon2) < circle_radius_in_km):
                flag=False
        if flag:
            final_specific_points.append(sorted_co_ordinates[i])
    return final_specific_points


# Function to convert selected coordinates to a DataFrame
def coordinate_dataframe(specific_points_coordinaes):
    data = pd.DataFrame(columns=["Lat", "Long", "Count", "Avg_speed"])

    # Loop through selected coordinates
    for i in range(len(specific_points_coordinaes)):
        cordinate, count, avg_speed = specific_points_coordinaes[i]
        lat, long = cordinate  # Extract latitude and longitude from the list
        data.loc[i] = [lat, long, count, avg_speed]  # Add data to DataFrame

    return data


if __name__ == "__main__":
    warn = ["data seperated on collisions\cas_fcw.csv", "data seperated on collisions\cas_hmw.csv",
            "data seperated on collisions\cas_ldw.csv", "data seperated on collisions\cas_pcw.csv"]
    for i in warn:
        # Read the CSV file into a DataFrame
        print("Currently working on : ", i)
        df = pd.read_csv(i, dtype={'Lat': float, 'Long': float})
        # Find unique coordinates and calculate average speed
        unique = df[['Lat', 'Long']].drop_duplicates()
        arr_to_store_unique_coord_with_avgspeed = []

        for index, row in unique.iterrows():
            lat = row['Lat'].round(8)
            long = row['Long'].round(8)

            matching_rows = df[(df['Lat'] == lat) & (df['Long'] == long)]
            avg_speed = matching_rows['Speed'].mean()
            arr_to_store_unique_coord_with_avgspeed.append([lat, long, avg_speed])

        # Calculate specific coordinates within a certain distance and their statistics
        co_ordinates_count = specific_co_ordintes(arr_to_store_unique_coord_with_avgspeed, 0.500)

        # Select specific points based on criteria
        specific_points_coordinaes = specific_points(co_ordinates_count, True, 1, 0.500)

        # Convert selected points to a DataFrame
        final_data = coordinate_dataframe(specific_points_coordinaes)
        
        # Export data to a CSV file
        exp_name = i[(i.find("/") + 1):]
        final_data.to_csv(exp_name, index=False)
        print("Csv file has been generated for this  : ", i)



