import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from fpdf import FPDF
from kivy.core.window import Window
from kivy.uix.popup import Popup

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", size=14)
        self.cell(0, 10, "", ln=True, align="C")

class PDFAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

    
        self.add_widget(Label(
            text="📄 PDF Generator",
            font_size=24,
            size_hint_y=None,
            height=40
        ))

      
        self.add_widget(Label(
            text="Enter your text below:",
            size_hint_y=None,
            height=30
        ))

      
        self.text_input = TextInput(
            hint_text="Type your content here...",
            size_hint_y=0.6,
            multiline=True
        )
        self.add_widget(self.text_input)

      
        self.font_size_input = TextInput(
            hint_text="Font size (default 14)",
            size_hint_y=None,
            height=40,
            multiline=False,
            input_filter="int"
        )
        self.add_widget(self.font_size_input)

   
        self.generate_btn = Button(
            text="Generate PDF",
            size_hint_y=None,
            height=50,
            background_color=(0, 0.5, 0, 1)
        )
        self.generate_btn.bind(on_press=self.generate_pdf)
        self.add_widget(self.generate_btn)

    def generate_pdf(self, instance):
        user_text = self.text_input.text
        font_size = self.font_size_input.text.strip()

        try:
            font_size = int(font_size) if font_size else 14
        except ValueError:
            font_size = 14

        if not user_text.strip():
            self.show_popup("Error", "Please enter some text before generating PDF.")
            return

       
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=font_size)
        pdf.multi_cell(0, 10, txt=user_text)

        file_path = os.path.join(os.getcwd(), "output.pdf")
        pdf.output(file_path)

        self.show_popup("Success", f"PDF saved as:\n{file_path}")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class MyPDFApp(App):
    def build(self):
        Window.size = (400, 600)  # For desktop preview
        return PDFAppUI()

if __name__ == "__main__":
    MyPDFApp().run()
