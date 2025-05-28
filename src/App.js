import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Header from './components/Header/index';
import MainLayout from './components/MainLayout/index';
import './style.css';
import './index.css'
function main() {
    return (
        <div className="App">
            <Header />
            <MainLayout />
        </div>
    );
}

export default main;