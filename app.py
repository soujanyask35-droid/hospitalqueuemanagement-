import gradio as gr
import pandas as pd

# Simulated patient queue
patient_queue = []

# AI logic to assign priority based on symptoms and age
def assign_priority(name, age, symptoms):
    priority_keywords = ['chest pain', 'shortness of breath', 'bleeding', 'unconscious', 'severe']
    priority = 3  # Default: Low

    print("\n--- Decision Log ---")
    print(f"Patient: {name}, Age: {age}, Symptoms: {symptoms}")

    # Check symptoms for high priority
    for keyword in priority_keywords:
        if keyword in symptoms.lower():
            priority = 1  # High priority
            print(f"Matched keyword '{keyword}' → Priority set to HIGH (1)")
            break

    # Check age for medium priority
    if priority == 3 and age > 65:
        priority = 2  # Medium priority for elderly
        print("Age > 65 and no critical symptoms → Priority set to MEDIUM (2)")

    if priority == 3:
        print("No critical symptoms and age <= 65 → Priority remains LOW (3)")

    patient = {
        'Name': name,
        'Age': age,
        'Symptoms': symptoms,
        'Priority': priority
    }

    patient_queue.append(patient)
    sorted_queue = sorted(patient_queue, key=lambda x: x['Priority'])

    # Convert to DataFrame for table display
    df = pd.DataFrame(sorted_queue)
    print("Current Queue (sorted by priority):")
    print(df)
    print("--- End of Decision Log ---\n")

    return df

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🏥 AI Hospital Queue Management System")
    gr.Markdown("Enter patient details below. The system will assign a priority and display the current queue.")

    with gr.Row():
        name = gr.Textbox(label="Patient Name", placeholder="e.g. John Doe")
        age = gr.Number(label="Age", precision=0)
        symptoms = gr.Textbox(label="Symptoms", placeholder="e.g. chest pain, fever")

    submit = gr.Button("Add to Queue")
    output = gr.Dataframe(headers=["Name", "Age", "Symptoms", "Priority"], label="Current Queue", interactive=False)

    submit.click(fn=assign_priority, inputs=[name, age, symptoms], outputs=output)

demo.launch()