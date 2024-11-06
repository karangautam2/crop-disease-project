import { Button } from "./components/ui/button";
import background from "./assets/plant.jpg"

export function Home({setState}){
    return (
        <div  className="pt-44 w-screen h-screen bg-no-repeat bg-cover" style={{backgroundImage: `url(${background})`}}>
            <div className="flex space-y-7 flex-col text-white justify-center items-center">
                <div className="font-bold text-3xl">Welcome to Smart Crop Disease Detection System</div>
                <div className="font-semibold text-2xl">Guidance to any type of Crop Disease</div>
                <div className="flex flex-col justify-center items-center text-xl">
                    <div>Developing a new model to this smart era, to reduce the burden of farmers </div>
                    <div>and to increase the yield with great solutions.</div>
                </div>
                <div>
                    <Button onClick={() => setState(2)}>Check Now!</Button>
                </div>
            </div>
        </div>
    )
}