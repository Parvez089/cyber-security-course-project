# app.py: Streamlit Web UI with Advanced Visuals

import streamlit as st
from cipher import encrypt, decrypt
from stego import hide_data, extract_data, get_difference_map
import io

st.set_page_config(page_title="CryptoStego Tool", page_icon="🔐", layout="wide")

st.title("🔐 Advanced Image Steganography & Cipher Tool")
st.markdown("Securely hide encrypted text messages inside images using **LSB Steganography**, **Vigenere Cipher**, and **Visual Analytics**.")

menu = st.sidebar.selectbox("Choose Task", ["Hide Secret Message (Encode)", "Extract Secret Message (Decode)"])

if menu == "Hide Secret Message (Encode)":
    st.subheader("📥 Hide an Encrypted Message in an Image")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "avif"])
        secret_text = st.text_area("Enter Secret Message", placeholder="Type your confidential message here...")
        cipher_key = st.text_input("Enter Encryption Key (Password)", type="password")
        
    with col2:
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Original Uploaded Image", use_container_width=True)

    if st.button("🚀 Encrypt & Hide Message"):
        if uploaded_file is not None and secret_text and cipher_key:
            encrypted_msg = encrypt(secret_text, cipher_key)
            image_bytes = uploaded_file.getvalue()
            try:
                stego_image_bytes = hide_data(image_bytes, encrypted_msg)
                
                st.balloons()
                st.success("✨ Message successfully encrypted and hidden in the image!")
                
                st.markdown("---")
                st.subheader("📊 Visual Comparison & Analysis")
                
                comp_col1, comp_col2, comp_col3 = st.columns(3)
                
                with comp_col1:
                    st.image(uploaded_file, caption="1. Original Image", use_container_width=True)
                
                with comp_col2:
                    st.image(stego_image_bytes, caption="2. Stego Image (With Hidden Data)", use_container_width=True)
                
                with comp_col3:
                    diff_img = get_difference_map(image_bytes, stego_image_bytes)
                    st.image(diff_img, caption="3. Visual Residual / Difference Map", use_container_width=True)
                
                st.info("💡 Note: The Residual Map highlights the modified pixel bits where the secret payload is embedded.")

                st.download_button(
                    label="📥 Download Stego Image (PNG)",
                    data=stego_image_bytes,
                    file_name="secret_stego_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("⚠️ Please upload an image, enter a secret message, and provide an encryption key.")

elif menu == "Extract Secret Message (Decode)":
    st.subheader("📤 Extract and Decrypt Message from an Image")
    
    col_ext1, col_ext2 = st.columns(2)
    
    with col_ext1:
        uploaded_file = st.file_uploader("Upload the Stego Image", type=["png", "jpg", "jpeg", "avif"])
        cipher_key = st.text_input("Enter Decryption Key (Password)", type="password")
        
    with col_ext2:
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Stego Image", use_container_width=True)
            
    if st.button("🔓 Extract & Decrypt Message"):
        if uploaded_file is not None and cipher_key:
            image_bytes = uploaded_file.getvalue()
            try:
                extracted_ciphertext = extract_data(image_bytes)
                original_message = decrypt(extracted_ciphertext, cipher_key)
                
                st.success("🎉 Message successfully extracted and decrypted!")
                st.text_area("🔓 Recovered Secret Message", original_message, height=150)
            except Exception as e:
                st.error(f"❌ Failed to extract message. Ensure the correct image and key are provided.")
        else:
            st.warning("⚠️ Please upload the stego image and enter the decryption key.")