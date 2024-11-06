import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Button } from "./components/ui/button"
import { Home } from './Home'
import { NavBar } from './NavBar'
import { Upload } from './Upload'
import { Toaster } from 'sonner'

function App() {
  const [nav, setNav] = useState(1)

  return (
    <div >
            <NavBar setState={setNav}></NavBar>
      {nav === 1 && <Home setState={setNav}></Home>}
{nav === 2 && <Upload />}
<Toaster></Toaster>
    </div>
  )
}

export default App
