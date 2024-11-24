import React, { useReducer, useRef, useState } from 'react'
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import baseUrl from '../baseUrl'
import toast from 'react-hot-toast';

function Process() {

    const [sessions, setSessions] = useState([])
    const [showInput, setShowInput] = useState(false)
    const [text, setText] = useState('')
    const [fLoading, setFLoading] = useState(false)
    const [uploadComplete, setUploadComplete] = useState(false)
    const [entities, setEntities] = useState(null)
    const [selectedEntities, setSelectedEntities] = useState(null)

    const fileRef = useRef(null)

    const addSession = () => {
        const oldSessions = sessions.slice()
        oldSessions.push({ fileName: 'Session '+parseInt(oldSessions.length+1)})
        setSessions(oldSessions)
    }

    const uploadFile = (e) => {
        const formData = new FormData()
        if (text) {
            formData.append('text', text)
        } else {
            formData.append('file', e.target.files[0])
        }
        setFLoading(true)
        fetch(baseUrl+'/process_input', {
            method: 'POST',
            headers: { 'Authorization': sessionStorage.getItem('token') },
            body: formData
        }).then(res => res.json())
        .then(response => {  
            setEntities(response)
            setSelectedEntities(response?.entities||[])
            setUploadComplete(true)          
        })
        .catch(err => {
            console.log(err);
            toast.error('Try Again!')
        }).finally(() => setFLoading(false))
    }

  return (
    <div className='bg-white h-[calc(100vh_-_100px)] w-full px-10 pb-4 flex flex-row items-center justify-between overflow-hidden'>
      <div className='shadow-sm w-[22%] h-full border bg-white rounded-md py-2 px-4'>
        <h3 className='w-full text-left font-semibold text-sm py-1 mb-2 flex items-center space-x-2'>
            <span className='text-md'>History</span>
            <button 
                onClick={() => addSession()}
                className='border border-black rounded-md px-1 text-sm text-center text-black bg-white hover:border-rose-600 flex flex-row items-center space-x-1'>
                <span>New Session</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="size-4">
                <path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" />
                </svg>
            </button>
        </h3>
        <div className={`w-full h-full flex flex-col items-center ${sessions.length===0?'justify-center':''} space-y-1`}>
            {
                sessions.length === 0 && (<div className='w-full flex flex-col items-center justify-center space-y-1'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6 text-gray-600">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <h2 className='w-full text-gray-600 text-center text-sm font-medium'>You have no sessions</h2>
                <p className='w-full text-gray-500 text-center text-xs font-light'>start one to use filter it now</p>
            </div>)
            }
            {
                sessions.map((session, index) => (
                    <div 
                        key={session?._id||index}
                        className='w-full rounded-md bg-gray-100 cursor-pointer text-left flex flex-row items-start justify-start py-1 px-1'>
                        <div className='rounded-md flex flex-row items-center justify-center p-1 space-x-1'>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-gray-500">
                                <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                                <path d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                            </svg>
                            <p className='text-center text-xs text-gray-600 whitespace-nowrap'>{session.fileName||'Session '+index+1}</p>
                        </div>
                    </div>
                ))
            }
        </div>
      </div>
      <div className='shadow-sm w-[35%] h-full overflow-y-auto border border-gray-300 bg-white rounded-md flex flex-col items-center py-4 px-4 space-y-3'>
        <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-gray-200 rounded-md text-black'>Input</p>
        {
            uploadComplete ? null : ( 
                <div className='w-full flex flex-row items-center space-x-1 ml-12'>            
                    <input accept='application/pdf,plain/text' multiple={false} ref={fileRef} onChange={e => uploadFile(e)} type='file' className='hidden' />
                    <button 
                        onClick={() => fileRef?.current?.click()}
                        className='border border-black rounded-md px-1 text-sm text-center text-black bg-white hover:border-rose-600 flex flex-row items-center space-x-1'>
                        Upload File
                    </button>
                    <p onClick={() => setShowInput(true)} className='hover:underline cursor-pointer px-2 text-sm text-black'>Enter Your Own Text</p>
                </div>
            )
        }
        {
            showInput && (
                <div className='w-full flex flex-row items-center space-x-1 ml-10'>            
                    <textarea 
                        value={text}
                        onChange={e => setText(e.target.value)}
                        rows={4}
                        className='w-full max-w-[90%] px-2 py-1 text-sm text-black outline-rose-300 resize-none rounded-md' placeholder='Enter your own text'></textarea>
                </div>
            )
        }
        {
            (fLoading || uploadComplete) && (
                <div className='w-full flex flex-row items-center'>
                    {fLoading ? (<div className='ml-1 w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div>):(
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                            <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
                        </svg>
                    )}
                    <p className='px-2 text-xs text-black'>{uploadComplete?'Uploaded':'Uploading'} File {uploadComplete?'':'...'}</p>
                </div>
            )
        }
        <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-gray-200 rounded-md text-black'>Sensitivity Detected</p>
        <div className='w-full flex flex-row items-center'>
            {/* <div className='w-2 h-2 bg-black rounded-full animate-ping duration-10 mr-2'></div> */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 text-black">
                <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clipRule="evenodd" />
            </svg>
            <p className='px-2 text-xs text-black'>Extracted sensitive information for parameters</p>
            
        </div>
        <p className='w-full text-xs px-2 text-black'>Deselect all the information that you want llm to know about.</p>
        <div className='w-full flex flex-col rounded-md border p-2'>
            {
                Object.keys(entities?.entities||{})?.map(item => (
                    <div className='w-full flex items-center space-x-1'>
                        <input onChange={e => setSelectedEntities(prev => ({...prev, [item]: entities.entities[item] }))} checked={selectedEntities.hasOwnProperty(item)} type='checkbox' className='rounded-md text-sm' />
                        <span className='text-sm'>{item}{': '}{entities.entities[item]}</span>
                    </div>
                ))
            }
        </div>
        {/* <p className='w-full max-w-[90%] mx-auto py-1 text-left text-xs px-2 bg-black rounded-md text-gray-100'>Custom Information</p> */}
        <p className='px-6 text-left w-full text-xs text-black'>Do you want to continue for summarizing ?</p>
        <div className='w-full px-6 flex flex-row items-start space-x-2'>
            <button onClick={() => console.log(selectedEntities)
            } className='bg-black text-white px-2 py-1 rounded-md text-xs'>Continue</button>
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
      </div>
      <div className='shadow-sm w-[40%] h-full border border-gray-300 rounded-md bg-white flex flex-col items-center justify-center'>
        <div className='w-full flex flex-col items-center justify-center space-y-1'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6 text-gray-500">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
            <h2 className='w-full text-gray-500 text-center text-sm font-medium'>Your Preview Window</h2>
            {/* <p className='w-full text-gray-500 text-center text-xs font-light'>start one to use filter it now</p> */}
        </div>
      </div>
    </div>
  )
}

export default Process
