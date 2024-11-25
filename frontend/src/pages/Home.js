import React, { useEffect, useRef, useState } from 'react'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'
import Typewriter from 'typewriter-effect/dist/core'

function Home() {

    const fileRef = useRef(null)
    const router = useNavigate()

    const [uploading, setUploading] = useState(false)

    useEffect(() => {
        new Typewriter('#subtext', {
            strings: ['information', '[PARAMETER]'],
            autoStart: true,
            loop: true,
            cursorClassName: 'text-white',
            pauseFor: 3000
          });
    }, [])

    const handleChange = (e) => {
        const file = e.target.files[0]
        setUploading(true)
        setTimeout(() => {
            setUploading(false)
            router('/process')
        }, 3000)
    }

  return (
    <div className='bg-white h-[calc(100vh_-_100px)] w-full px-10 py-8 flex flex-col items-center'>
        <div className='w-full min-h-[400px] flex flex-col items-center space-y-1'>
            <h2 className='max-w-[60%] mx-auto text-center text-black text-4xl leading-tight font-medium tracking-tighter'>
                Protect your valuable <span className='text-3xl' id='subtext'>information</span> <br/>from public <span className=''>Text Generation Models</span>
            </h2>
            <p className='text-center text-gray-500 text-sm'>Filter, Process and Use your data with any commercial AI tools with ease.</p>
            <br />
            <input 
                ref={fileRef}
                type='file' 
                multiple={false}
                accept='application/pdf'
                style={{ display: 'none' }} 
                onChange={e => handleChange(e)}
            />
            <div 
                onClick={() => sessionStorage.getItem('token')?router('/process'):toast.error("Authenticate to continue")}
                className='max-w-[300px] cursor-pointer hover:shadow-md hover:border-rose-600 rounded-md border border-black p-3 flex flex-col items-start space-y-2'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                </svg>
                <h2 className='w-full text-left text-md text-black font-semibold'>
                    Summarizer
                </h2>
                <p className='text-sm text-gray-500 text-left w-full'>Summarize your reports, audits and other documents or texts</p>
            </div>
            {/* {
                uploading ? (
                    <img src='./uploading.gif' className='contain h-[100px]' />
                ) : (
                    <button 
                        onClick={() => fileRef?.current?.click()}
                        className='transform transition duration-500 ease-out scale-100 opacity-100 active:scale-0 active:opacity-0 hover:bg-red-600 rounded-md bg-red-500 text-sm text-white px-4 py-2 flex flex-row items-center space-x-3'>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-white">
                            <path d="M9.25 13.25a.75.75 0 0 0 1.5 0V4.636l2.955 3.129a.75.75 0 0 0 1.09-1.03l-4.25-4.5a.75.75 0 0 0-1.09 0l-4.25 4.5a.75.75 0 1 0 1.09 1.03L9.25 4.636v8.614Z" />
                            <path d="M3.5 12.75a.75.75 0 0 0-1.5 0v2.5A2.75 2.75 0 0 0 4.75 18h10.5A2.75 2.75 0 0 0 18 15.25v-2.5a.75.75 0 0 0-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5Z" />
                        </svg>
                        <span className='text-white font-medium'>Upload</span>
                    </button>
                )
            } */}
        </div>
        <div className='relative flex flex-row items-center'>
            <div className='rounded-md flex flex-col items-center justify-center p-1 space-y-1 w-[100px] h-[100px]'>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-gray-500 mb-2">
                    <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                    <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                </svg>
                <p className='w-full text-center text-xs text-gray-600'>Record.pdf</p>
            </div>
            <img
                src='./right-arrow.png'
                className='contain h-[30px] mx-4'
            />
            <div className='rounded-md ml-2 text-xs px-2 py-2 w-[150px] text-center border border-gray-400 border-dashed flex flex-col items-center justify-center bg-white shadow-sm'>
                <p>extracted pdf content here for further process</p>
            </div>
            <img
                src='./right-arrow.png'
                className='contain h-[30px] mx-4'
            />
            <div className='w-[100px] relative bg-black bottom-2'>
                <img src='./py.jpeg' className='rounded-full bg-white w-[30px] h-[30px] absolute -top-4' />
                <img src='./spacy.png' className='rounded-full bg-white w-[40px] h-[40px] absolute left-7 -top-1' />
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6 rounded-full text-sky-500 absolute top-4 left-2">
                    <path d="M17.004 10.407c.138.435-.216.842-.672.842h-3.465a.75.75 0 0 1-.65-.375l-1.732-3c-.229-.396-.053-.907.393-1.004a5.252 5.252 0 0 1 6.126 3.537ZM8.12 8.464c.307-.338.838-.235 1.066.16l1.732 3a.75.75 0 0 1 0 .75l-1.732 3c-.229.397-.76.5-1.067.161A5.23 5.23 0 0 1 6.75 12a5.23 5.23 0 0 1 1.37-3.536ZM10.878 17.13c-.447-.098-.623-.608-.394-1.004l1.733-3.002a.75.75 0 0 1 .65-.375h3.465c.457 0 .81.407.672.842a5.252 5.252 0 0 1-6.126 3.539Z" />
                    <path fillRule="evenodd" d="M21 12.75a.75.75 0 1 0 0-1.5h-.783a8.22 8.22 0 0 0-.237-1.357l.734-.267a.75.75 0 1 0-.513-1.41l-.735.268a8.24 8.24 0 0 0-.689-1.192l.6-.503a.75.75 0 1 0-.964-1.149l-.6.504a8.3 8.3 0 0 0-1.054-.885l.391-.678a.75.75 0 1 0-1.299-.75l-.39.676a8.188 8.188 0 0 0-1.295-.47l.136-.77a.75.75 0 0 0-1.477-.26l-.136.77a8.36 8.36 0 0 0-1.377 0l-.136-.77a.75.75 0 1 0-1.477.26l.136.77c-.448.121-.88.28-1.294.47l-.39-.676a.75.75 0 0 0-1.3.75l.392.678a8.29 8.29 0 0 0-1.054.885l-.6-.504a.75.75 0 1 0-.965 1.149l.6.503a8.243 8.243 0 0 0-.689 1.192L3.8 8.216a.75.75 0 1 0-.513 1.41l.735.267a8.222 8.222 0 0 0-.238 1.356h-.783a.75.75 0 0 0 0 1.5h.783c.042.464.122.917.238 1.356l-.735.268a.75.75 0 0 0 .513 1.41l.735-.268c.197.417.428.816.69 1.191l-.6.504a.75.75 0 0 0 .963 1.15l.601-.505c.326.323.679.62 1.054.885l-.392.68a.75.75 0 0 0 1.3.75l.39-.679c.414.192.847.35 1.294.471l-.136.77a.75.75 0 0 0 1.477.261l.137-.772a8.332 8.332 0 0 0 1.376 0l.136.772a.75.75 0 1 0 1.477-.26l-.136-.771a8.19 8.19 0 0 0 1.294-.47l.391.677a.75.75 0 0 0 1.3-.75l-.393-.679a8.29 8.29 0 0 0 1.054-.885l.601.504a.75.75 0 0 0 .964-1.15l-.6-.503c.261-.375.492-.774.69-1.191l.735.267a.75.75 0 1 0 .512-1.41l-.734-.267c.115-.439.195-.892.237-1.356h.784Zm-2.657-3.06a6.744 6.744 0 0 0-1.19-2.053 6.784 6.784 0 0 0-1.82-1.51A6.705 6.705 0 0 0 12 5.25a6.8 6.8 0 0 0-1.225.11 6.7 6.7 0 0 0-2.15.793 6.784 6.784 0 0 0-2.952 3.489.76.76 0 0 1-.036.098A6.74 6.74 0 0 0 5.251 12a6.74 6.74 0 0 0 3.366 5.842l.009.005a6.704 6.704 0 0 0 2.18.798l.022.003a6.792 6.792 0 0 0 2.368-.004 6.704 6.704 0 0 0 2.205-.811 6.785 6.785 0 0 0 1.762-1.484l.009-.01.009-.01a6.743 6.743 0 0 0 1.18-2.066c.253-.707.39-1.469.39-2.263a6.74 6.74 0 0 0-.408-2.309Z" clipRule="evenodd" />
                </svg>
            </div>
            <img src='./right-d-arrow.png' className='contain h-[70px] mr-2' />
            <div className='relative flex flex-col items-start space-y-1 px-2'>
                <span className='rounded-md text-xs text-black flex flex-row items-center space-x-1 text-left'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3 h-3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Personal</span>
                </span>
                <span className='rounded-md text-xs text-black flex flex-row items-center space-x-1 text-left'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3 h-3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Organisation</span>
                </span>
                <span className='rounded-md text-xs text-black flex flex-row items-center space-x-1 text-left'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3 h-3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Custom</span>
                </span>
            </div>
            <img
                src='./right-arrow.png'
                className='contain h-[30px] mx-4'
            />
            <div className='flex flex-row items-center space-x-2'>
                <img src='./openai.png' className='rounded-full bg-white w-[40px] h-[40px] border border-gray-400' />
                <img src='./mongodb.webp' className='rounded-full bg-white w-[40px] h-[40px] p-1 border border-gray-400' />
                
            </div>
            <div className='relative'>
                <img
                    src='./right-arrow.png'
                    className='contain h-[30px] mx-4 transform rotate-[-30deg] absolute -top-10'
                />
                <img
                    src='./right-arrow.png'
                    className='contain h-[30px] mx-4 transform'
                />
                <img
                    src='./right-arrow.png'
                    className='contain h-[30px] mx-4 transform rotate-[30deg] absolute -bottom-10'
                />
            </div>
            <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1'>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                    <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                    <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                </svg>
                <p className='text-center text-xs text-gray-600'>Protected-Record.pdf</p>
            </div>
            <div className='relative'>
                <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1 absolute -top-14 -right-4'>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                        <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                        <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                    </svg>
                    <p className='text-center text-xs text-gray-600 whitespace-nowrap'>Summarized-Content.pdf</p>
                </div>
            </div>
            <div className='relative'>
                <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1 absolute top-8 right-2'>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                        <path fillRule="evenodd" d="M4.848 2.771A49.144 49.144 0 0 1 12 2.25c2.43 0 4.817.178 7.152.52 1.978.292 3.348 2.024 3.348 3.97v6.02c0 1.946-1.37 3.678-3.348 3.97a48.901 48.901 0 0 1-3.476.383.39.39 0 0 0-.297.17l-2.755 4.133a.75.75 0 0 1-1.248 0l-2.755-4.133a.39.39 0 0 0-.297-.17 48.9 48.9 0 0 1-3.476-.384c-1.978-.29-3.348-2.024-3.348-3.97V6.741c0-1.946 1.37-3.68 3.348-3.97ZM6.75 8.25a.75.75 0 0 1 .75-.75h9a.75.75 0 0 1 0 1.5h-9a.75.75 0 0 1-.75-.75Zm.75 2.25a.75.75 0 0 0 0 1.5H12a.75.75 0 0 0 0-1.5H7.5Z" clipRule="evenodd" />
                    </svg>
                    <p className='text-center text-xs text-gray-600 whitespace-nowrap'>Chat with document</p>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Home
