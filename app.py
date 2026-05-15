import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image

# title part
st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload upto 3 images to generate Note Summary and Quizzes")
st.divider()

# image upload part
with st.sidebar:
    st.header("Controls")
    images = st.file_uploader("Uppload the photos of your note", 
                     type=['jpg', 'jpeg', 'png'],
                     accept_multiple_files=True)
    pil_images = []
    # image processing exeption handling
    try:
        if images:
            for img in images:
                pil_img = Image.open(img)
                pil_images.append(pil_img)
    except Exception as e:
        st.error(f"Error while processing images: {e}")

    else: 
        if images:
            if len(images) > 3:
                st.error("Cannot upload more than 3 images")
            else:
                st.subheader("Uploaded images")

                col = st.columns(len(images))

                for i, image in enumerate(images):
                    with col[i]:
                        st.image(image)

    # difficulty catagory part
    selected_option = st.selectbox("Enter the difficulty level of your quiz",
                 ("Easy","Medium","Hard"),
                 index=None)
    

    
    pressed = st.button("Click the button to initiate AI", type='primary')


if pressed:
    if not images:
        st.error("You must upload image first")
    
    if not selected_option:
        st.error("You must select a difficulty level")

    else:
        try:

        # note
            with st.container(border=True):
                st.subheader("Your note Summary", anchor=False)

            # the portion below will be replaced by API call
                with st.spinner("AI is writing note summary for you"):
                    generated_notes = note_generator(pil_images)
                    st.markdown(generated_notes)

        # audio transcript
            with st.container(border=True):
                st.subheader("Audio transcription", anchor=False)
             # the portion below will be replaced by API call
                with st.spinner("AI is making audio transcription for you"):
                # clearing the markdown
                    generated_notes = str(generated_notes)
                    generated_notes = generated_notes.replace("#","")
                    generated_notes = generated_notes.replace("*","")
                    generated_notes = generated_notes.replace("-","")
                    generated_notes = generated_notes.replace("$","")
                    generated_notes = generated_notes.replace("`","")
                    generated_notes = generated_notes.replace('"',"")
                
                    audio_transcript = audio_transcription(generated_notes)
                    st.audio(audio_transcript)

        # quiz
            with st.container(border=True):
                st.subheader(f"Quiz questions (Difficulty Level: {selected_option}):", anchor=False)
             # the portion below will be replaced by API call
                with st.spinner("AI is generating quizzes for you"):
                    quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
        
        