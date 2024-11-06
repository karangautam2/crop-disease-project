from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from torchvision import transforms
import timm
import io
from PIL import Image
import torch

app = FastAPI()

# Allow all origins for simplicity. Adjust the origins list to your needs.
origins = [
    "*"
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the preprocess function
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to 224x224 pixels
    transforms.ToTensor(),          # Convert the image to a PyTorch tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Normalize with mean and std
                         std=[0.229, 0.224, 0.225])
])

classes = {'Corn___Common_Rust': 0,
 'Corn___Gray_Leaf_Spot': 1,
 'Corn___Healthy': 2,
 'Corn___Northern_Leaf_Blight': 3,
 'Potato___Early_Blight': 4,
 'Potato___Healthy': 5,
 'Potato___Late_Blight': 6,
 'Rice___Brown_Spot': 7,
 'Rice___Healthy': 8,
 'Rice___Leaf_Blast': 9,
 'Rice___Neck_Blast': 10,
 'Sugarcane_Bacterial Blight': 11,
 'Sugarcane_Healthy': 12,
 'Sugarcane_Red Rot': 13,
 'Wheat___Brown_Rust': 14,
 'Wheat___Healthy': 15,
 'Wheat___Yellow_Rust': 16}

disease_solutions = {
    'https://content.ces.ncsu.edu/corn-rusts-common-and-southern-rust#:~:text=Management%201%20Resistant%20Varieties%20The%20most%20cost-effective%20method,leaves%20observed%20have%20one%20or%20more%20pustules.%20': 0,  # Corn___Common_Rust
    'https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/gray-leaf-spot-on-corn/#:~:text=Effective%20management%20of%20Gray%20leaf%20spot%20involves%20the,in%20no%20till%20fields%2C%20fungicides%20may%20be%20considered.': 1,  # Corn___Gray_Leaf_Spot
    'https://livetoplant.com/common-corn-plant-diseases-how-to-identify-and-treat/#:~:text=Using%20fungicides%2C%20crop%20rotation%2C%20and%20genetic%20resistance%20are,plant%20growth%20and%20maximum%20yield%20for%20your%20crops.': 2,  # Corn___Healthy
    'https://ohioline.osu.edu/factsheet/plpath-cer-10#:~:text=Management%201%20Planting%20resistant%20hybrids%20is%20the%20most,dent%20corn%20fields%20planted%20with%20susceptible%20hybrids.%20': 3,  # Corn___Northern_Leaf_Blight
    'https://ipm.cahnr.uconn.edu/early-blight-and-late-blight-of-potato/#:~:text=Early%20blight%20of%20potato%20is,found%20on%20older%20leaves%20first': 4,  # Potato___Early_Blight
    'https://vikaspedia.in/agriculture/crop-production/package-of-practices/vegetables-1/potato': 5,  # Potato___Healthy
    'https://ipm.cahnr.uconn.edu/early-blight-and-late-blight-of-potato/#:~:text=Early%20blight%20of%20potato%20is,found%20on%20older%20leaves%20first.': 6,  # Potato___Late_Blight
    'http://www.agritech.tnau.ac.in/expert_system/paddy/cpdisbrownspot.html': 7,  # Rice___Brown_Spot
    'https://ccari.icar.gov.in/dss/rice.html': 8,  # Rice___Healthy
    'http://www.agritech.tnau.ac.in/expert_system/paddy/cpdisblast.html': 9,  # Rice___Leaf_Blast
    'https://extension.missouri.edu/publications/mp645': 10,  # Rice___Neck_Blast
    'https://www.aphis.usda.gov/plant-pests-diseases/sugarcane-disease': 11,  # Sugarcane_Bacterial Blight
    'https://iisr.icar.gov.in/iisr/aicrp/pages/aicrp_crop_production.htm': 12,  # Sugarcane_Healthy
    'https://agritech.tnau.ac.in/crop_protection/sugarcane_diseases/sugarcane_d4.html#:~:text=Symptoms%3A,of%20the%20leaf%20midrib%20also.': 13,  # Sugarcane_Red Rot
    'https://www.cropscience.bayer.us/articles/cp/wheat-rust-diseases': 14,  # Wheat___Brown_Rust
    'https://www.tribiome.eu/a-nutritional-plan-for-a-healthy-productive-wheat-crop/': 15,  # Wheat___Healthy
    'https://agritech.tnau.ac.in/crop_protection/wheat/crop_prot_crop%20diseases_cereals_wheat_3.html': 16  # Wheat___Yellow_Rust
}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        model = timm.create_model("rexnet_150", pretrained=True, num_classes=len(classes))
        model.load_state_dict(torch.load("./crop_best_model.pth", map_location=torch.device('cpu'), weights_only=True))
        model.eval()
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")  # Ensure the image is in RGB mode
        input_tensor = preprocess(image) 
        input_tensor = input_tensor.unsqueeze(0)  # Add a batch dimension for the single image

        with torch.no_grad():
            output = model(input_tensor)
            pred_class = torch.argmax(output, dim=1).item()
            class_name = list(classes.keys())[list(classes.values()).index(pred_class)]
            disease_link = list(disease_solutions.keys())[list(disease_solutions.values()).index(pred_class)]
            return JSONResponse(content={"predicted_class": class_name, "remedy": disease_link})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
