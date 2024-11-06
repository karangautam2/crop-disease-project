import { Title } from "@radix-ui/react-dialog";
import { Button } from "./components/ui/button";

export function NavBar({ setState }) {
  return (
    <div className="flex w-full fixed h-10 justify-start items-center">
      <Button variant="link" onClick={() => setState(1)} className="font-bold text-white px-8" >Crop Disease Detection</Button>
      <Button variant="link" unClick={() => setState(2)} className="font-bold text-white px-8" >Contact</Button>
    </div>
  );
}
 