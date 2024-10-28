import React from 'react'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from './pages/Home';
import Header from './components/Header';
import Process from './pages/Process';
import Settings from './pages/Settings';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/' Component={Home} />
        <Route path='/process' Component={Process} />
        <Route path='/settings' Component={Settings} />
        <Route path='/about' Component={About} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
