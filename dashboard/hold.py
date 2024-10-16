   def calculate_visibility(test_max_visibility, test_cloud_coverage, test_time_step, test_orbital_frequency):
        orbital_effect = np.sin(2 * np.pi * test_orbital_frequency * test_time_step)
        visibility = test_max_visibility * (1 - test_cloud_coverage / 100) * (0.5 + 0.5 * orbital_effect)
        return visibility

    bodies = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Moon', 'Pluto']
    max_visibilities = [12000, 25000, 30000, 20000, 18000, 15000, 13000, 30000, 10000]
    orbital_frequencies = [0.2, 0.1, 0.05, 0.07, 0.03, 0.02, 0.01, 0.5, 0.005]

    start_date = pd.Timestamp('2024-11-01')
    end_date = pd.Timestamp('2024-11-30')
    days = pd.date_range(start=start_date, end=end_date, freq='D')

    data = []
    for body, max_visibility, frequency in zip(bodies, max_visibilities, orbital_frequencies):
        for i, day in enumerate(days):
            cloud_coverage = np.random.randint(0, 100)
            visibility = calculate_visibility(max_visibility, cloud_coverage, i, frequency)
            data.append({
                'body_name': body,
                'date': day,
                'max_visibility_m': max_visibility,
                'cloud_coverage_percent': cloud_coverage,
                'visibility_m': visibility
            })


    visibility_df = pd.DataFrame(data)

    source = pd.DataFrame({
        'x': visibility_df['date'].dt.date,  
        'y': visibility_df['body_name'],     
        'z': visibility_df['visibility_m']    
    })


    heatmap = alt.Chart(source).mark_rect().encode(
        x=alt.X('x:O', title='Date', axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('y:O', title='Celestial Body'),
        color=alt.Color('z:Q',
                        scale=alt.Scale(domain=[0, 30000],
                                        range=['#fff5eb', '#ff0000', '#800080']),
                        title='Visibility (m)'),
        tooltip=['y', 'x:T', 'z']
    ).properties(
        width=2000,
        height=500,
        title='Daily Visibility of Celestial Bodies'
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        st.altair_chart(heatmap, use_container_width=True)
