import * as React from "react"

import { Button } from "./components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import { Toaster, toast } from "sonner"
import background from "./assets/farmer.jpg"
import { DiseaseDialog } from "./Disease"



export function Upload() {
  const [disease, setDisease]
 = React.useState("");
 const [remedy, setRemedy]
 = React.useState("");

 const [open, setOpen] = React.useState(false);

  async function handleFileChange(event){
    const file = event.target.files[0];
    const form = new FormData();
    form.append("file", file);
    const promise =  fetch("http://localhost:8000/predict", {method: "POST", body: form});
    toast.promise(promise, {
      loading: "Checking Disease.....",
      success: "Disease Checked !",
      error: "Failed to Check Disease !"
      
    })
    promise
    .then((res) => res.json())
    .then((disease) => {
      setDisease(disease.predicted_class); 
      setRemedy(disease.remedy); 
      setOpen(true)
    })
    .catch((err) => console.log("Error while checking disease : ", err));
  }

  
  return (
    <div className="flex justify-center pt-44 h-screen bg-cover"   style={{backgroundImage: `url(${background})`}}>
    <Card className="w-[50vw] h-fit bg-transparent text-white justify-between">
      <CardHeader>
        <CardTitle>Upload image to test for disease</CardTitle>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="name">Crop Image</Label>
              <Input id="name" placeholder="Name of your project" type="file" onChange={handleFileChange}/>
            </div>
          </div>
        </form>
      </CardContent>
      {/* <CardFooter className="flex justify-between">
        <Button onClick={() => toast("Checking for disease....")} variant="secondary">Upload</Button>
      </CardFooter> */}
    </Card>
    <DiseaseDialog onOpen={setOpen} openState={open} disease={disease} remedy={remedy}></DiseaseDialog>
    </div>
  )
}
