import { useEffect, useState } from 'react'
import "./App.css"
import Header from './components/Header'
import BodyComponent from './components/BodyComponent'
import { BrowserRouter, Outlet, Route, Routes } from 'react-router';
import FileUpload from './components/Pages/FileUpload/FileUpload';
import Dashboard from './components/Pages/Dashboard/Dashboard';
import Section1 from './components/Pages/Dashboard/Sections/Section1/index';
import Section2 from './components/Pages/Dashboard/Sections/Section2/index';
import Section3 from './components/Pages/Dashboard/Sections/Section3/index';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<FileUpload/>}></Route>

        <Route path='/dashboard' element={<Dashboard/>}>
          <Route path='section1' element={<Section1></Section1>}></Route>
          <Route path='section2' element={<Section2></Section2>}></Route>
          <Route path='section3' element={<Section3></Section3>}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
