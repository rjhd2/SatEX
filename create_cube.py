latdim=hourly_data[0].coord('latitude') 
londim=hourly_data[0].coord('longitude')
attri={"creator_name": "Veronika Portge", "creator_email": "veronika.portge@metoffice.gov.uk"}
LSTmax_reshaped=np.reshape(LSTmax, (1,LSTmax.shape[0], LSTmax.shape[1]))
LSTmin_reshaped=np.reshape(LSTmin, (1,LSTmin.shape[0], LSTmin.shape[1]))

timedim=hourly_data[0].coord('time')

LSTmaxcube=iris.cube.Cube(LSTmax_reshaped, long_name="Maximum Land Surface Temperature (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])
LSTmincube=iris.cube.Cube(LSTmin_reshaped, long_name="Minimum Land Surface Temperature (PMW)", units="K", attributes=attri, dim_coords_and_dims=[(timedim, 0), (latdim, 1), (londim, 2)])

cubelist=iris.cube.CubeList([LSTmaxcube, LSTmincube])
