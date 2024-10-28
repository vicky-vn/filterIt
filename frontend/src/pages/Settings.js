import React from 'react'

function Settings() {
  return (
    <div className='bg-white h-full min-h-[calc(100vh_-_100px)] w-full px-10 pb-4 flex flex-row items-start justify-between space-x-4'>
      <div className='w-1/2 h-full flex flex-col items-center'>
        <div className='w-full bg-gray-100 text-left rounded-md mb-3'>
            <p className='w-full text-left text-sm text-black px-2 py-1'>Public Text Generation Model</p>
        </div>
        <div className='w-full flex flex-row items-center flex-wrap space-x-2'>
            <div className='bg-black rounded-md flex flex-row items-center cursor-pointer justify-center py-1 px-2 space-x-1 border-2 hover:border-black border-rose-500'>
                <img src='./openai.png' className='contain h-[30px] invert' />
                <p className='text-center text-xs text-gray-100 whitespace-nowrap'>Open AI</p>
            </div>
            <div className='bg-orange-100 rounded-md flex flex-row items-center cursor-pointer justify-center py-1 px-2 space-x-1 border hover:border-black'>
                <img src='./claude.png' className='contain h-[30px]' />
                <p className='text-center text-xs text-black whitespace-nowrap'>Claude AI</p>
            </div>
        </div>
      </div>
      <div className='w-1/2 h-full grid grid-rows-2 gap-4'>
        <div>
            <div className='w-full bg-gray-100 text-left rounded-md'>
                <p className='w-full text-left text-sm text-black px-2 py-1'>Organisational Information</p>
            </div>
            <div className='w-full border h-[300px] my-2'>
                <textarea
                    className='w-full h-full text-left bg-black rounded-md px-2 py-2 text-sm text-white'
                    placeholder='Separated by new line'
                ></textarea>
            </div>
        </div>
        <div>
            <div className='w-full bg-gray-100 text-left rounded-md'>
                <p className='w-full text-left text-sm text-black px-2 py-1'>Custom Information</p>
            </div>
            <div className='w-full border h-[300px] my-2'>
                <textarea
                    className='w-full h-full text-left bg-black rounded-md px-2 py-2 text-sm text-white'
                    placeholder='Separated by new line'
                ></textarea>
            </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
