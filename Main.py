import streamlit as st
from streamlit_option_menu import option_menu
import tempfile
import easyocr
import re
import cv2
import base64
import mysql.connector
import pandas as pd
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt


st.set_page_config(layout='wide',page_title= "business_cardsX",page_icon= '🧑‍💻')

# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("https://images.unsplash.com/photo-1557683304-673a23048d34?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1700&q=80");
# background-size: 180%;
# background-position: top left;
# background-repeat: no-repeat;
# background-attachment: local;

# }}

# [data-testid="stHeader"] {{
# background: rgba(0,0,0,0);
# }}

# </style>
# """


# st.markdown(page_bg_img, unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: orange; font-size: 50px'>business_cardsX : Business Card Data Extraction</h1>", unsafe_allow_html=True)
st.write("")

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS business_cardsx")
cursor.execute("USE business_cardsx")
cursor.execute('''CREATE TABLE IF NOT EXISTS business_cards (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    designation VARCHAR(255),
                    company_name VARCHAR(255),
                    contact VARCHAR(20),
                    alternative VARCHAR(20),
                    email VARCHAR(255),
                    website VARCHAR(255),
                    street VARCHAR(255),
                    city VARCHAR(255),
                    state VARCHAR(255),
                    pincode VARCHAR(10),
                    image MEDIUMTEXT)''')
conn.commit()

selected = option_menu(None, ["Home", "Upload", "Database", "Settings"], 
    icons=['house', 'cloud-upload', "database", "gear"], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://miro.medium.com/v2/resize:fit:720/format:webp/1*x94FIYwbCo7OebWU3pWh8w.png",width= 650)
    with col2:
        st.write("hi hello")

if selected == "Upload":
    
    reader = easyocr.Reader(['en'])
    uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "png", "jpeg"],accept_multiple_files= False)
       
    # To create imported image in temporary FilePath
    if uploaded_file:
        temp_file = tempfile.NamedTemporaryFile(delete = False)
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

        # Read text from the uploaded image
        extracted_text = reader.readtext(image_path)

        if extracted_text:
            st.write("Extracted Text:")
            data = []
            for i in range(len(extracted_text)):
                data.append(extracted_text[i][1])
            # # st.code(data)
        name = []
        designation = []
        contact =[]
        email =[]
        website = []
        street =[]
        city =[]
        state =[]
        pincode=[]
        company =[]

        for i in range(len(data)):
            match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)',data[i])    
            match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', data[i])
            match3 = re.findall('^[E].+[a-z]',data[i])
            match4 = re.findall('([A-Za-z]+) ([0-9]+)',data[i])
            match5 = re.findall('([0-9]+ [a-zA-z]+)',data[i])    
            match6 = re.findall('.com$' , data[i])
            match7 = re.findall('([0-9]+)',data[i])
            if data[i] == data[0]:
                name.append(data[i])        
            elif data[i] == data[1]:
                designation.append(data[i])
            elif '-' in data[i]:
                contact.append(data[i])
            elif '@' in data[i]:
                email.append(data[i])
            elif "www " in data[i].lower() or "www." in data[i].lower():
                website.append(data[i])
            elif "WWW" in data[i]:
                website.append(data[i] +"." + data[i+1])
            elif match6:
                pass
            elif match1:
                street.append(match1[0][0])
                city.append(match1[0][1])
                state.append(match1[0][2])
            elif match2:
                street.append(match2[0][0])
                city.append(match2[0][1])
            elif match3:
                city.append(match3[0])
            elif match4:
                state.append(match4[0][0])
                pincode.append(match4[0][1])
            elif match5:
                street.append(match5[0]+' St,')
            elif match7:
                pincode.append(match7[0])
            else:
                company.append(data[i])
        if len(company)>1:
            comp = company[0]+' '+company[1]
            st.code(comp)
        else:
            comp = company[0]
        if len(contact) >1:
            contact_number = contact[0]
            alternative_number = contact[1]
        else:
            contact_number = contact[0]
            alternative_number = None
        
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Convert the binary image data to a base64 encoded string
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        name = name[0]
        designation = designation[0]
        company_name = comp
        contact = contact_number
        alternative = alternative_number
        email = email[0]
        website = website[0]
        street = street[0]
        city = city[0]
        state = state[0]
        pincode = pincode[0]
        image = encoded_image


        col3, col4 = st.columns(2)

        with col3:
            if uploaded_file: 
                st.image(uploaded_file, caption="Uploaded Image", use_column_width= True)
                img = cv2.imread(image_path)

                #detection in extracted_text

                for detection in extracted_text:    
                    top_left =tuple([int(val) for val in detection[0][0]])
                    bottom_right =tuple([int(val) for val in detection[0][2]])
                    text = detection[1]
                    font =cv2.FONT_HERSHEY_SIMPLEX
                    img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 2)
                    img = cv2.putText(img, text, top_left, font, 1, (255,0,0),1, cv2.LINE_AA)
                    plt.figure(figsize=(20,20))
                st.image(img)

        with col4:
            
            st.write('**Name** :', name)
            st.write('**Designation** :', designation)
            st.write('**Company Name** :', company_name)
            st.write('**Contact Number** :', contact)
            st.write('**Alternative Number** :', alternative)
            st.write('**E-mail** :', email)
            st.write('**Website** :', website)
            st.write('**Street** :', street)
            st.write('**City** :', city)
            st.write('**State** :', state)
            st.write('**Pincode** :', pincode)
            st.write("")
            st.write("")

            if st.button("Upload"):
                #st.code("ok")
                query = f"SELECT email FROM business_cards WHERE email = '{email}';"
                cursor.execute(query)
                result = cursor.fetchone()

                if result is not None:
                    st.warning("Duplicate Data, Data already exists", icon="⚠")
                else:
                    # Insert the data into the 'business_cards' table
                    insert_query = "INSERT INTO business_cards (name, designation, company_name, contact, alternative, email, " \
                                "website, street, city, state, pincode, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                "%s, %s)"
                    values = (name, designation, company_name, contact, alternative, email, website, street, city, state,
                            pincode, image)
                    cursor.execute(insert_query, values)
                    conn.commit()
                    st.warning("Data successfully added", icon ='✅')
if selected == "Database":
    
    query = "SELECT * FROM business_cards;"
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    st.header("Database")                    
    st.dataframe(df)
    st.button('Refresh Data')

    st.subheader("To Edit DataBase")
    edit = option_menu(None, ["Modify Data", "Delete Data"], 
    icons=['database-fill-gear', 'database-dash'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    
    # edit = st.radio(" ",["Modify Data", "Delete Data"])

    if edit == "Modify Data":  
        st.header("Modify")   
        col5, col6 = st.columns(2)
        with col5:
            names= ['Choose Categories','name','designation','email','company_name']
            selected = st.selectbox('**Select Categories**',names)
            try:
                if selected != 'Choose Categories':
                    select = df[selected]
                    select_detail = st.selectbox('**Select Details**', select)
                    st.header('Select the modify details')
                    df1 = df[df[selected] == select_detail]
                    df1 = df1.reset_index()
                    select_modify = st.selectbox('**Select categories**', df.columns)
                    a = df1[select_modify][0]            
                    st.write(f'Do you want to change {select_modify}: **{a}** ?')
                    modified = st.text_input(f'**Enter the {select_modify}**')
                    if modified:
                        st.write(f'{select_modify} **{a}** changed as **{modified}**')
                    if st.button("Commit Changes"):
                        cursor.execute(f"update business_cards set {select_modify} = '{modified}' where {selected} = '{select_detail}' ;")
                        conn.commit()
                        st.success("Data successfully updated", icon ='✅')
                else:
                    select_detail = st.selectbox('**Select details**', "")
                
                    st.header('Select the modify details')
                    select_modify = st.selectbox('**Select categories**', '')
                    modified = st.text_input('')
            except KeyError:
                pass
            try:
                with col6:
                    if selected != '':
                        image_data = df[df[selected] == select_detail]
                        image_data = image_data.reset_index()
                        encoded_image = image_data['image'][0] # Get the base64 encoded image data from the DataFrame
                        convert = base64.b64decode(encoded_image) # Decode the base64 encoded image data back to binary
                        image = Image.open(io.BytesIO(convert)) # Open the image using PIL
                        st.image(image)
            except KeyError:
                pass
    if edit == "Delete Data":
        st.header("Delete Data")  
        names= ['','name','email']
        delete_selected = st.selectbox('**Select Name**',names) 
        if delete_selected != '':
            
            select = df[delete_selected]
            delete_select_detail = st.selectbox('**Select Details**', select)
            st.write(f'Do you want to delete **{delete_select_detail}** card details ?')
            col5,col6,col7 =st.columns([1,1,5])
            delete = col5.button('Yes')
            delete1 = col6.button('No')
            if delete:
                delete_query = f"delete from business_cards where {delete_selected} = '{delete_select_detail}'"
                cursor.execute(delete_query)
                conn.commit()
                st.success("Data Deleted successfully", icon ='✅')
        else:
            st.selectbox('**Select Details**', ' ')
if selected == "Settings":
    st.write("settings")
    