import React from 'react'
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';

function Process() {
  return (
    <div className='bg-white h-[calc(100vh_-_100px)] w-full px-10 pb-4 flex flex-row items-center justify-between'>
      <div className='shadow-sm w-[22%] h-full border bg-white rounded-md bg-white py-2 px-4'>
        <h3 className='w-full text-left font-semibold text-sm py-1 mb-2'>Documents</h3>
        <div className='w-full flex flex-col items-center space-y-1'>
            <div className='w-full rounded-md bg-gray-100 cursor-pointer text-left flex flex-row items-start justify-start py-1 px-1'>
                <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1'>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                        <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                        <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                    </svg>
                    <p className='text-center text-xs text-gray-600 whitespace-nowrap'>Record123.pdf</p>
                </div>
            </div>
            <div className='w-full rounded-md hover:bg-gray-100 cursor-pointer text-left flex flex-row items-start justify-start py-1 px-1'>
                <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1'>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                        <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                        <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                    </svg>
                    <p className='text-center text-xs text-gray-600 whitespace-nowrap'>Record343.pdf</p>
                </div>
            </div>
        </div>
      </div>
      <div className='shadow-sm w-[35%] h-full border border-gray-300 bg-white rounded-md bg-white flex flex-col items-center py-4 px-4 space-y-3'>
        <div className='w-full flex flex-row items-center'>
            {/* <div className='ml-1 w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div> */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
            </svg>
            <p className='px-2 text-xs text-black'>Uploading Record123.pdf ...</p>
        </div>
        <div className='w-full flex flex-row items-center'>
            {/* <div className='w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div> */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
            </svg>
            <p className='px-2 text-xs text-black'>Exracting sensitive information for parameters ...</p>
        </div>
        <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-gray-200 rounded-md text-black'>Personal Information</p>
        <div className='w-full flex flex-wrap items-center px-6 space-x-2'>
            <span className='rounded-md bg-gray-600 text-xs text-white px-2'>Vignesh</span>
            <span className='rounded-md bg-gray-600 text-xs text-white px-2'>vignesh@gmail.com</span>
        </div>
        <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-gray-200 rounded-md text-black'>Organisation Information</p>
        <div className='w-full flex flex-wrap items-center px-6 space-x-2'>
            <span className='rounded-md bg-gray-600 text-xs text-white px-2'>Windsor Hospital</span>
        </div>
        <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-gray-200 rounded-md text-black'>Geographical Information</p>
        <div className='w-full flex flex-wrap items-center px-6 space-x-2'>
            <span className='rounded-md bg-gray-600 text-xs text-white px-2'>N9C 3H2</span>
            <span className='rounded-md bg-gray-600 text-xs text-white px-2'>Ontario</span>
        </div>
        {/* <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-black rounded-md text-gray-100'>Custom Information</p> */}
        <div className='w-full flex flex-row items-center'>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
            </svg>
            {/* <div className='ml-1 w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div> */}
            <p className='w-full px-2 text-xs text-black'>Saving your parameters to the database ...</p>
        </div>
        <p className='px-6 text-left w-full text-xs text-black'>Do you want to continue using OpenAI ?</p>
        <div className='w-full px-6 flex flex-row items-start space-x-2'>
            <button className='bg-black text-white px-2 py-1 rounded-md text-xs'>Continue</button>
            <span className='text-gray-600 text-xs py-1 text-center'>-or-</span>
            <button className='text-black py-1 rounded-md text-xs'><span className=''>Download</span> <span className='underline'>Protected-Record.pdf</span></button>
        </div>
        <div className='w-full flex flex-row items-center'>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
            </svg>
            {/* <div className='ml-1 w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div> */}
            <p className='w-full px-2 text-xs text-black'>Connecting to OpenAI ...</p>
        </div>
        <div className='px-6 w-full flex flex-wrap space-x-2'>
            <button className='rounded-md bg-white border border-black text-xs text-black px-2 hover:bg-black hover:text-white'>Summarize</button>
            <button className='rounded-md bg-white border border-black text-xs text-black px-2 hover:bg-black hover:text-white'>Ask a question</button>
        </div>
        <input className='w-full ml-12 text-xs text-black text-left outline-none' placeholder='Enter your question' />
        <p className='w-full px-6 text-xs text-black'>John is 20 years old</p>
      </div>
      <div className='shadow-sm w-[40%] h-full border border-gray-300 bg-white rounded-md bg-white'>
        <div className='py-4'></div>
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
            <Viewer fileUrl="https://pdfobject.com/pdf/sample.pdf" />
        </Worker>
      </div>
    </div>
  )
}

export default Process
