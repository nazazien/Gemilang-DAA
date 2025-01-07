from keperluan_modul import *

bg()

with st.sidebar:
    page = option_menu(
        menu_title="Main Menu",  
        options=["Home", "Price Estimation", "About Us"],
        icons=["house","bar-chart","people"],
        menu_icon="menu-button", 
        default_index=0,
    )
    
    st.write(':grey[Review💬]')
    messages = st.container(height=200)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)                
    comments = [ "UI-nya simpel, jadi gampang dipake 😍", "Membantu bangett 💪", "Aku emang butuh web ini 🙌", "Cepet banget hasilnya ⚡", "Prediksinya pas banget sama yang aku cari 🔥", "Web ini keren banget sih 😎", "Aplikasinya baguss 👍", "Sangat berguna buat aku 😊", "Ini kan aplikasi buat prediksi harga jual mobil 🚗" ]
    for comment in comments:
        messages.chat_message("user").write(comment)
    

if page == "Home":  
    pemanis.ucapan()  

    col1,col2,col3 = st.columns([2,0.1,4])
    with col1: 
        st.write(' ')
        st.image(Image.open('Documents/image/g2.png'),width=200)
    with col2:
        st.header('| ')
    with col3:
        st.write(' ')        
        st.subheader(' How We Can Help You?')

    st.write('')
    st.title(':rainbow[HOW MUCH IS MY CAR COST?]')
    st.write(':grey[Friday, 08 November 2023. By [gemilang.com](http://localhost:8501/%F0%9F%91%A5%20About%20Us)]')    
    
    video_file = open("Documents/video/profilnew.mp4", "rb")
    video_bytes = video_file.read()    
    st.video(video_bytes)
    
    st.subheader('Find Your Car Price')
    col1,col2 = st.columns([2,2])
    with col1:        
        st.write('Gemilang, our application is for those of you who are confused about determining the selling price of a used TOYOTA car quickly and accurately. Check the estimated price of your car carefully before selling your car')

    with col2:        
        st.image(Image.open('Documents/image/left.png'), width=350)        
    
    st.subheader('Promoting Your Used Car')    
    col1,col2,col3 = st.columns([2,2,2])
    with col1:
        st.image(Image.open('Documents/image/1.png'), width=250)
        st.write('Accurate price estimates: Entering the details of the vehicle you want to sell will produce an immediate selling price that matches the market.')

    with col2:
        st.image(Image.open('Documents/image/2.png'), width=250)
        st.write('Save Time: No need to search for prices for a long time, simply entering the car details will produce an accurate price.')

    with col3:
        st.image(Image.open('Documents/image/3.png'), width=250)
        st.write('Right price: Provides benefits for both parties so that no one feels disadvantaged and can compete in the market.')    

elif page == "Price Estimation":    
    st.header(':rainbow[PRICE ESTIMATION]', divider='rainbow')
    st.subheader('Predict the price of your used Toyota car here!')
    st.subheader('')

    df = pd.read_csv('Documents/data/toyota.csv')    

    def dac(df, feature, threshold, toleransi=1):
        lower_part = df[df[feature] <= threshold + toleransi]
        upper_part = df[df[feature] > threshold - toleransi]
        return lower_part, upper_part
    
    def bobot(X, Y, regularization_strength):
        X_T = matriks.transpose(X)
        X_T_X = matriks.matrix_multiplication(X_T, X)
        X_T_Y = matriks.matrix_multiplication(X_T, [[y] for y in Y])

        for i in range(len(X_T_X)):
            X_T_X[i][i] += regularization_strength

        X_T_X_inv = matriks.matrix_inverse(X_T_X)
        W = matriks.matrix_multiplication(X_T_X_inv, X_T_Y)
        return [w[0] for w in W]
    
    def prediksi(features, weights):
        return sum(f * w for f, w in zip(features, weights))

    def hitung_mse(harga, prediksi):    
        kuadrat_error = 0
        for i in range(len(harga)):
            kuadrat_error += (harga[i] - prediksi[i]) ** 2
        mse = kuadrat_error / len(harga)
        return mse
    
    def hitung_mape(actual_prices, predicted_prices):                       
        total_percentage_error = 0
        n = len(actual_prices)
        
        for actual, predicted in zip(actual_prices, predicted_prices):                
            if actual != 0:
                percentage_error = abs((actual - predicted) / actual)
                total_percentage_error += percentage_error
        
        mape = (total_percentage_error / n) * 100
        return mape

    normalisasi_kolom = ['mileage', 'tax', 'mpg', 'engineSize', 'year']
    df, normalisasi_data = normalisasi.normalize_data(df, normalisasi_kolom)
    encodings = normalisasi.encode_categorical_variables(
        df, target_col='price', feature_cols=['model', 'transmission', 'fuelType']
    )
    train_df, test_df = normalisasi.train_test_split(df)

    garis = st.container(border=True)
    col1,col2 = garis.columns([2,2])
    with col1:
        year = st.number_input('Enter Car Year        : ')
        mileage = st.number_input('Enter mileage (km)  : ')
        tax = st.number_input('Enter Car Tax        : ')
        mpg = st.number_input('Enter Car Fuel Consumption : ')
        engineSize = st.number_input('Enter Engine Size       : ')
    
    with col2:
        st.image(Image.open('Documents/image/terbang.png'), caption='https://www.freepik.com/pikaso')        

    model = garis.selectbox('Select Car Model', list(encodings['model'].keys()))
    transmission = garis.selectbox('Select Transmission Type', list(encodings['transmission'].keys()))
    fuelType = garis.selectbox('Select Fuel Type', list(encodings['fuelType'].keys()))
    
    if year == 0 or mileage == 0 or tax == 0 or mpg == 0 or engineSize == 0 or not model or not transmission or not fuelType:
        st.warning("Masukkan Spesifikasi Mobil Anda!.")
        st.image(Image.open('Documents/image/so.png'), caption='Source: https://storyset.com/')        
    else:    
        year = normalisasi.normalize_input(year, *normalisasi_data['year'])
        mileage = normalisasi.normalize_input(mileage, *normalisasi_data['mileage'])
        tax = normalisasi.normalize_input(tax, *normalisasi_data['tax'])
        mpg = normalisasi.normalize_input(mpg, *normalisasi_data['mpg'])
        engineSize = normalisasi.normalize_input(engineSize, *normalisasi_data['engineSize'])

        user_features = [
            1, mileage, year, engineSize, mpg, tax,
            encodings['model'][model], encodings['transmission'][transmission], encodings['fuelType'][fuelType]
        ]
    
        thresholds = {
            'year': year if year else df['year'].median(),
            'engineSize': engineSize if engineSize else df['engineSize'].median(),
            'mileage': mileage if mileage else df['mileage'].median(),
            'mpg': mpg if mpg else df['mpg'].median(),
        }

        subset = train_df
        for feature, threshold in thresholds.items():
            subset, _ = dac(subset, feature, threshold)
            # st.write(f"Feature: {feature}, Threshold: {threshold}")        
            # st.write(subset)
            # st.write(f"Number of Rows: {subset.shape[0]}")

        if len(subset) < 100:
            st.error("Masukkan data yang valid.")
            st.image(Image.open('Documents/image/so.png'), caption='Source: https://storyset.com/') 
        else:
            X, Y = matriks.prepare_matrices(subset)
            weights = bobot(X, Y, regularization_strength=0.01)
            Y_pred = [prediksi(features, weights) for features in X]
            mse = hitung_mse(Y, Y_pred)
            
            estimasi = prediksi(user_features, weights)
            if estimasi < 0:
                st.error("Masukkan data yang valid.")
                st.image(Image.open('Documents/image/so.png'), caption='Source: https://storyset.com/') 
            else:
                pemanis.sukses()

                st.subheader('', divider='rainbow')
                gambar, hasil = st.columns([2, 2])
                with gambar:
                    st.image(Image.open('Documents/image/oe.png'), width=350, caption='Source: https://storyset.com/')
                with hasil:
                    st.subheader(':rainbow[ESTIMATED PRICE : ]')
                    st.title(f'$ {estimasi:,.0f}')
                    st.write("Model Mean Squared Error (MSE):", mse)
                    mape = hitung_mape(Y, Y_pred)
                    st.write("Mean Absolute Percentage Error (MAPE): ")
                    st.write(round(mape, 2), "%")
                    # st.write(weights)
                    
                    data = {
                        'Actual Price': Y,
                        'Predicted Price': Y_pred
                    }
                    export = pd.DataFrame(data)
                    base_folder = os.path.expanduser("~\\Documents\\data")
                    os.makedirs(base_folder, exist_ok=True)                    
                    path = os.path.join(base_folder, "prediksi.xlsx")                    
                    export.to_excel(path, index=False, engine='openpyxl')
                    
                    with open(path, "rb") as file:
                        st.download_button(
                            label="📄 Export to Excel",
                            data=file,
                            file_name="prediksi.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                st.subheader('', divider='rainbow')


elif page == "About Us":    
    pemanis.profil()

    st.header(':rainbow[ABOUT US]', divider='rainbow')
    st.subheader('We are behind the scenes of Gemilang!')
    st.subheader("")

    deskripsi, poto = st.columns([3,2])
    with deskripsi:
        st.markdown('''The “Gemilang” team consists of three students from the 2023E Bachelor of Data Science Study Program, Faculty of Mathematics and Natural Sciences, Surabaya State University.
This team was formed with the aim of fulfilling the third semester final assignment in the Algorithm Analysis Design course under the guidance of Mrs. Dr. Elly Matul Imah, M.Kom.
The project carried out by this team is "Implementation and Analysis of the Divide and Conquer Algorithm in the Used Toyota Car Price Prediction System".
The “Gemilang” team hopes to make a positive contribution in completing this third semester final assignment.
''')

    with poto:
        st.image(Image.open('Documents/image/G.png'), width=250)
    
    st.markdown('''Our Vision
Become a trusted solution for predicting used car prices.
\n
Our Mission
Create an easy-to-use used car price prediction tool.
Help sellers determine the right price.
Increase our knowledge through practical experience.''')
    st.subheader("",divider='grey')
    st.subheader(":rainbow[Our Team]", divider='grey')

    col1,col2,col3 = st.columns([2,2,2])
    with col1:
        st.image(Image.open('Documents/image/naza.jpg'), width=150)
        st.markdown('''Naza Sulthoniyah Wahda
                    23031554026
                    naza.23026@gmail.com''')

    with col2:
        st.image(Image.open('Documents/image/salwa.jpeg'), width=150)
        st.markdown('''Salwa Nadhifah Az Zahrah
                    23031554136
                    salwa.23136@mhs.unesa.ac.id''')

    with col3:
        st.image(Image.open('Documents/image/salsa.jpg'), width=150)
        st.markdown('''Salsabilla Indah Rahmawati
                    23031554193
                    salsabilla.23193@mhs.unesa.ac.id''')
