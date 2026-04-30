1
!pip install docling langchain-core langchain-community opencv-python-headless
!pip install transformers torch torchvision 
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

print("Environment Ready.")

# --- CELL ---
2
import pandas as pd
import os

base_dir = '/kaggle/input/datasets/raddar/chest-xrays-indiana-university' 
reports_csv = os.path.join(base_dir, 'indiana_reports.csv')
projections_csv = os.path.join(base_dir, 'indiana_projections.csv')

reports_df = pd.read_csv(reports_csv)
projections_df = pd.read_csv(projections_csv)

def parse_clinical_report_csv(uid):
    """
    Fetches the findings, impression, and associated images for a given report UID.
    """
    report_data = {
        "uid": uid,
        "image_filenames": [],
        "findings": "Not provided",
        "impression": "Not provided"
    }
    
    # 1. Locate the text report for this UID
    report_row = reports_df[reports_df['uid'] == uid]
    
    if not report_row.empty:
        # Extract findings and impression, handling potential NaN (empty) values
        findings = report_row.iloc[0]['findings']
        impression = report_row.iloc[0]['impression']
        
        report_data["findings"] = findings if pd.notna(findings) else "Not provided"
        report_data["impression"] = impression if pd.notna(impression) else "Not provided"
        
    # 2. Locate all images associated with this UID in the projections table
    image_rows = projections_df[projections_df['uid'] == uid]
    if not image_rows.empty:
        report_data["image_filenames"] = image_rows['filename'].tolist()
        
    return report_data

sample_uid = reports_df['uid'].iloc[0]
sample_data = parse_clinical_report_csv(sample_uid)

print("Parsed Report Data:")
print(f"UID: {sample_data['uid']}")
print(f"Associated Images: {sample_data['image_filenames']}")
print(f"Findings: {sample_data['findings']}")
print(f"Impression: {sample_data['impression']}")

# --- CELL ---
3
image_dir = os.path.join(base_dir, 'images', 'images_normalized')

if sample_data["image_filenames"]:
    # Grab the first image associated with the report
    img_filename = sample_data["image_filenames"][0]
    img_path = os.path.join(image_dir, img_filename)
    
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        plt.figure(figsize=(8,8))
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title(f"X-Ray: {img_filename}")
        plt.show()
    else:
        print(f"Image {img_filename} not found in {image_dir}")
else:
    print("No images associated with this report.")

# --- CELL ---
5
!pip install ultralytics
import cv2
from ultralytics import YOLO
import matplotlib.patches as patches

# --- CELL ---
6
# Load a pre-trained YOLO model (downloads automatically in Kaggle if internet is on)
# We use a 'nano' or 'small' model first for rapid testing
model = YOLO('yolov8n.pt') 

print("Vision Model Loaded.")

# --- CELL ---
7
# Ensure we have the image path from your previous pandas data dictionary
if sample_data["image_filenames"]:
    img_filename = sample_data["image_filenames"][0]
    img_path = os.path.join(image_dir, img_filename)
    
    # 1. Run inference on the X-Ray
    results = model(img_path)
    
    # 2. Load image for plotting
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    
    # 3. Extract bounding boxes and plot them
    boxes = results[0].boxes.xyxy.cpu().numpy() # Get coordinates (x1, y1, x2, y2)
    classes = results[0].boxes.cls.cpu().numpy() # Get class IDs
    
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        width, height = x2 - x1, y2 - y1
        
        # Create a Rectangle patch
        rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        
        # Optional: Add label (will be generic COCO labels for now until fine-tuned)
        ax.text(x1, y1-5, f"Detection {int(classes[i])}", color='red', fontsize=12, weight='bold')

    plt.title(f"Vision Layer Detection: {img_filename}")
    plt.show()
    
    print(f"Detected {len(boxes)} regions of interest.")

# --- CELL ---
9
import yaml
import os
import glob
from ultralytics import YOLO

# 1. Automatically hunt down the data.yaml file anywhere in the Kaggle input directory
print("Hunting for dataset...")
yaml_files = glob.glob('/kaggle/input/**/data.yaml', recursive=True)

if not yaml_files:
    print("❌ Could not find data.yaml! Double check that the dataset is mounted in the right panel.")
else:
    # Get the exact path where the dataset actually lives
    original_yaml = yaml_files[0]
    base_dataset_dir = os.path.dirname(original_yaml)
    print(f"✅ Found dataset exactly at: {base_dataset_dir}")

    # 2. Read their messy configuration
    with open(original_yaml, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # 3. Force the paths to be the exact, absolute paths we just auto-discovered
    yaml_data['train'] = os.path.join(base_dataset_dir, 'train')
    yaml_data['val'] = os.path.join(base_dataset_dir, 'val')
    
    # Safely handle the test folder (YOLO will crash if it expects a test folder that isn't there)
    if os.path.exists(os.path.join(base_dataset_dir, 'test')):
        yaml_data['test'] = os.path.join(base_dataset_dir, 'test')
    elif 'test' in yaml_data:
        del yaml_data['test'] 

    # 4. Save the bulletproof YAML to your working directory
    working_yaml_path = '/kaggle/working/bulletproof_medical_data.yaml'
    with open(working_yaml_path, 'w') as file:
        yaml.dump(yaml_data, file)

    print(f"✅ Bulletproof YAML saved to {working_yaml_path}")
    print("🚀 Starting YOLO Training...")

    # 5. Initialize and run the training loop
    model = YOLO('yolov8s.pt')
    
    results = model.train(
        data=working_yaml_path,
        epochs=25,                  
        imgsz=512,                  
        batch=16,                   
        device=0,                   
        project='/kaggle/working/', 
        name='medical_yolo_run',
        workers=2                   
    )

# --- CELL ---
10
from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import os

my_medical_model = YOLO('/kaggle/working/medical_yolo_run-2/weights/best.pt')

if sample_data["image_filenames"]:
    img_filename = sample_data["image_filenames"][0]
    img_path = os.path.join(image_dir, img_filename)
    
    # 3. Run inference!
    # conf=0.25 filters out low-confidence guesses
    results = my_medical_model(img_path, conf=0.25) 
    
    # 4. Plot the results
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    
    boxes = results[0].boxes.xyxy.cpu().numpy() 
    classes = results[0].boxes.cls.cpu().numpy()
    confidences = results[0].boxes.conf.cpu().numpy()
    
    detected_findings = []

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        width, height = x2 - x1, y2 - y1
        
        # Grab the medical name you just trained it to recognize
        class_id = int(classes[i])
        anomaly_name = my_medical_model.names[class_id]
        if anomaly_name != "No finding":
            detected_findings.append(anomaly_name)
            
            # Draw the box
            rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect)
            
            # Add label
            label_text = f"{anomaly_name} ({confidences[i]:.2f})"
            ax.text(x1, y1-5, label_text, color='red', fontsize=12, weight='bold', 
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
        # Draw the box
        rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        
        # Add label
        label_text = f"{anomaly_name} ({confidences[i]:.2f})"
        ax.text(x1, y1-5, label_text, color='red', fontsize=12, weight='bold', 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    plt.title(f"Custom YOLO Inference: {img_filename}")
    plt.show()
    
    print(f"Vision Layer Output: Detected {detected_findings}")

# --- CELL ---
12
import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from ultralytics import YOLO

# 1. Configuration
# Assuming 'image_dir' from Phase 1 is still in memory. If not, redefine it:
# image_dir = '/kaggle/input/chest-xrays-indiana-university/images/images_normalized'
model = YOLO('/kaggle/working/medical_yolo_run-2/weights/best.pt')
confidence_threshold = 0.25 # Only show relatively confident predictions
num_images_to_test = 6

# 2. Grab a random sample of images
all_images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
sample_images = random.sample(all_images, num_images_to_test)

# 3. Setup the Matplotlib Grid
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

print(f"Running Inference on {num_images_to_test} random images...")

for idx, img_filename in enumerate(sample_images):
    img_path = os.path.join(image_dir, img_filename)
    ax = axes[idx]
    
    # Run YOLO
    results = model(img_path, conf=confidence_threshold, verbose=False)
    
    # Load and show image
    img = mpimg.imread(img_path)
    ax.imshow(img, cmap='gray')
    ax.axis('off')
    
    # Extract data
    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()
    confidences = results[0].boxes.conf.cpu().numpy()
    
    findings_count = 0
    
    # Draw boxes
    for i, box in enumerate(boxes):
        class_id = int(classes[i])
        anomaly_name = model.names[class_id]
        
        if anomaly_name != "No finding":
            findings_count += 1
            x1, y1, x2, y2 = box
            width, height = x2 - x1, y2 - y1
            
            # Draw box
            rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect)
            
            # Draw label
            label_text = f"{anomaly_name} ({confidences[i]:.2f})"
            ax.text(x1, y1-5, label_text, color='red', fontsize=10, weight='bold', 
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.5))
    
    # Title logic
    if findings_count == 0:
        ax.set_title(f"Image: {img_filename}\n✅ No Findings Detected", color='green', weight='bold')
    else:
        ax.set_title(f"Image: {img_filename}\n⚠️ Detected {findings_count} Anomalies", color='red', weight='bold')

plt.tight_layout()
plt.show()

# --- CELL ---
14
!pip install langchain-mistralai

# --- CELL ---
15
!pip install -q langchain-google-genai langchain langchain-core

# --- CELL ---
16
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("GOOGLE_API_KEY")

# --- CELL ---
17
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

# 1. Pull the secret from Kaggle's vault
user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("GOOGLE_API_KEY")

# 2. THE MISSING LINK: Set the environment variable so LangChain can find it
os.environ["GOOGLE_API_KEY"] = secret_value_0
# Initialize Gemini 2.5 Flash 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

prompt_template = """
You are an expert medical communicator. Your task is to translate a dense radiologist report into a plain-language summary for a patient.

Here is the clinical report:
Findings: {clinical_findings}
Impression: {clinical_impression}

Here are the anomalies detected by our Computer Vision model on the patient's X-ray:
Detected Visual Anomalies: {vision_detections}

Instructions:
1. Write a patient-friendly summary of the Impression at a 6th-grade reading level.
2. If the Vision model detected an anomaly that matches the text report, explicitly mention that our AI also saw it on the scan.
3. If the report says everything is normal, reassure the patient clearly.
4. Do not provide medical advice or diagnoses. Add a disclaimer to consult a physician.

Patient Summary:
"""

prompt = PromptTemplate(
    input_variables=["clinical_findings", "clinical_impression", "vision_detections"],
    template=prompt_template,
)

chain = prompt | llm

# Let's test it using a simulated "Cardiomegaly" case based on your successful vision output
test_inputs = {
    "clinical_findings": "The heart size is enlarged. The aorta is tortuous and unfolded. Lungs are clear without focal consolidation, effusion, or pneumothorax.",
    "clinical_impression": "Cardiomegaly and aortic unfolding. No acute pulmonary disease.",
    "vision_detections": "Cardiomegaly, Aortic_enlargement" # Simulating the output from your top-middle image!
}

print("Generating Multimodal Patient Summary...\n")
response = chain.invoke(test_inputs)
print(response.content)