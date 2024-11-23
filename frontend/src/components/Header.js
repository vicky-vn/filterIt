import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Dialog, DialogPanel, DialogTitle, DialogBackdrop } from '@headlessui/react'
import { Toaster,toast } from 'react-hot-toast'
import baseUrl from '../baseUrl'

function Header() {

    const [openAuthDialog, setOpenAuthDialog] = useState(false)
    const [email, setEmail] = useState('')
    const [code, setCode] = useState('')
    const [isNew, setIsNew] = useState(false)
    const [qrCode, setQrCode] = useState(null)

    const handleAuth = () => {
        if (!email) {
            return toast.error('Invalid Email Address')
        }

        fetch(baseUrl+'/signup', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ email: email })
        })
        .then(res => res.json())
        .then(response => {
            if (response.error === '') {
                setIsNew(true)
            } else {
                setQrCode(response.qr_code_base64||null)
            }
        })
        .catch(err => toast.error('Authentication Failed'))
        // setOpenAuthDialog(false)
    }

  return (
    <div>
        <div className='w-full px-10 py-6 text-md flex flex-row items-center justify-between'>
            <div className='flex items-center space-x-2'>
                <img 
                    src='./logo.png'
                    alt='logo'
                    className='contain h-[30px]'
                />
                <Link to='/' className='flex items-center space-x-2'>
                    <h1 className='tracking-tighter text-2xl text-left text-black font-bold'>filterIt</h1>
                    <span className='font-light text-sm'>for</span>
                    <img src='./logo-wrh.png' className='h-10' />
                </Link>
            </div>
            <div className='flex flex-row items-center space-x-6'>
                <Link to='/'>
                    <p className='text-black text-sm text-center hover:text-gray-600'>Home</p>
                </Link>
                <Link to='/settings'>
                    <p className='text-black text-sm text-center hover:text-gray-600'>Settings</p>
                </Link>
                <Link to='/about'>
                    <p className='text-black text-sm text-center hover:text-gray-600'>About</p>
                </Link>
                <button 
                    onClick={() => setOpenAuthDialog(true)}
                    className='transform active:scale-105 duration-200 rounded-md text-xs font-medium text-white bg-black hover:bg-gray-700 text-center px-3 py-1 flex items-center space-x-1'>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-4">
                        <path fillRule="evenodd" d="M10 2a.75.75 0 0 1 .75.75v7.5a.75.75 0 0 1-1.5 0v-7.5A.75.75 0 0 1 10 2ZM5.404 4.343a.75.75 0 0 1 0 1.06 6.5 6.5 0 1 0 9.192 0 .75.75 0 1 1 1.06-1.06 8 8 0 1 1-11.313 0 .75.75 0 0 1 1.06 0Z" clipRule="evenodd" />
                        </svg>
                        <span>Authenticate</span>
                </button>
            </div>
            <Dialog open={openAuthDialog} as="div" className="relative z-10 focus:outline-none" onClose={() => {}}>
                <DialogBackdrop className="fixed inset-0 bg-black/50" />
                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                    <div className="flex min-h-full items-start justify-center p-4 mt-10">
                        <DialogPanel
                            transition
                            className="w-full max-w-lg rounded-md bg-white p-4 backdrop-blur-2xl duration-100 ease-out data-[closed]:transform-[scale(95%)] data-[closed]:opacity-0"
                        >
                        <DialogTitle as="h3" className="text-md mb-2 font-semibold text-black">
                            Authentication
                        </DialogTitle>
                        <label htmlFor='email' className='text-gray-500 text-left text-xs'>Organisation Email Address</label>
                        <input 
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            id='email'
                            type='email'
                            placeholder='user@company.com'
                            className='my-1 rounded-md outline-none border w-full text-left text-black text-xs px-3 py-2'
                        />
                        {
                            qrCode ? (
                                <img src={qrCode} className='' />
                            ) : (!qrCode && isNew) ? (
                                <>
                                    <label htmlFor='code' className='text-gray-500 text-left text-xs'>Verification Code</label>
                                    <input 
                                        value={code}
                                        onChange={e => setCode(e.target.value)}
                                        id='code'
                                        type='number'
                                        placeholder='6 digit code'
                                        className='my-1 rounded-md outline-none border w-full text-left text-black text-xs px-3 py-2'
                                    />
                                </>
                            ) : null
                        }
                        <div className="mt-4">
                            <button 
                                onClick={() => handleAuth()}
                                className='transform active:scale-105 duration-200 bg-black px-2 py-1 text-white text-center text-xs rounded-md mr-2'>Continue</button>
                            <button 
                                onClick={() => setOpenAuthDialog(false)}
                                className='transform active:scale-105 duration-200 bg-white px-2 py-1 text-black hover:bg-gray-100 text-center text-xs rounded-md mr-2'>Cancel</button>
                        </div>
                        </DialogPanel>
                    </div>
                </div>
            </Dialog>
        </div>
        <Toaster
            position="top-center"
            reverseOrder={false}
        />
    </div>
  )
}

export default Header
