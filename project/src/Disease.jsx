import { Button } from "./components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./components/ui/dialog"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"

export function DiseaseDialog({disease, onOpen, openState, remedy }) {
  return (
    <Dialog onOpenChange={onOpen} open={openState}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Disease</DialogTitle>
        </DialogHeader>
        <div className="text-lg">
     <div className="font-bold text-lg">{disease}</div>
        </div>
        <Button onClick={()=>window.open(remedy, "_blank")}>More Info</Button>
      </DialogContent>
    </Dialog>
  )
}
