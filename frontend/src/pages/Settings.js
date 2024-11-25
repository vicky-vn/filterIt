import React, { useEffect, useState } from 'react'
import baseUrl from '../baseUrl'
import toast from 'react-hot-toast'
import CustomItem from '../components/CustomItem'

function Settings() {

    const [orgE, setorgE] = useState(null)
    const [custE, setCusE] = useState([])
    const [showNew, setSN] = useState(false)
    const [llm, setLLM] = useState('openai')

    /**
     * Used to get all the entities that are tagged towards organisation of the user
     */
    useEffect(() => {
        async function getOrgEntities() {
            fetch(baseUrl+'/get_organizational_entity', {
                headers: { 'Authorization': 'Bearer '+sessionStorage.getItem('token') }
            })
            .then(res => res.json())
            .then(response => {
                setorgE(response?.organizational_entity?.terms.join('\n'))
            })
            .catch(err => {
                toast.error('Try Again')
                console.log(err);                
            })
        }
        getOrgEntities()
    }, [])

    /**
     * Used to get all the entities that are tagged as personalized or custom based on the user
     */
    async function getCustomEntties() {
        fetch(baseUrl+'/get_custom_entities', {
            headers: { 'Authorization': 'Bearer '+sessionStorage.getItem('token') }
        })
        .then(res => res.json())
        .then(response => {
            setCusE(response?.custom_entities||[])
        })
        .catch(err => toast.error('Try Again'))
    }
    useEffect(() => {
        
        getCustomEntties()
    }, [])

    /**
     * Used to add or update an entity for an organisational data
     */
    const addOrgEntity = () => {
        fetch(baseUrl+'/update_organizational_entity', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer '+sessionStorage.getItem('token') },
            body: JSON.stringify({ terms: orgE?.split('\n')||'', label: 'ORG' })
        }).then(res => res.json())
        .then(response => {
            toast.success('Entity Updated!')
        }).catch(err => {
            console.log(err);
            toast.error('try Again')
        })
    }

    /**
     * Used to store the choice of llm (text generation models) available publicly
     * for now only open ai is integerated
     * @param {string} e 
     */
    const saveLLMChoice = (e='openai') => {
        fetch(baseUrl+'/save_llm_choice', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer '+sessionStorage.getItem('token') },
            body: JSON.stringify({ llm_choice: e })
        }).then(res => res.json())
        .then(response => {
            setLLM(e)
            toast.success('LLM Choice Updated!')
        }).catch(err => {
            console.log(err);
            toast.error('try Again')
        })
    }

    /**
     * Used to add or update the existing entities that are tagged as custom ones for the user
     * @param {object} e 
     */
    const addcusEntity = (e) => {
        fetch(baseUrl+'//update_custom_entity', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer '+sessionStorage.getItem('token') },
            body: JSON.stringify(e)
        }).then(res => res.json())
        .then(response => {
            toast.success('Custom Entity Updated!')
        }).catch(err => {
            toast.error('try Again')
        })
    }

    useEffect(() => {
        if (orgE) {
            const timer = setTimeout(() => {
                addOrgEntity()
            }, 2000)
            return () => clearTimeout(timer)
        }
    }, [orgE])

  return (
    <div className='bg-white h-full min-h-[calc(100vh_-_100px)] w-full px-10 pb-4 flex flex-row items-start justify-between space-x-4'>
      <div className='w-1/2 h-full flex flex-col items-center'>
        <div className='w-full bg-gray-100 text-left rounded-md mb-3'>
            <p className='w-full text-left text-sm text-black px-2 py-1'>Public Text Generation Model</p>
        </div>
        <div className='w-full flex flex-row items-center flex-wrap space-x-2'>
            <div onClick={() => saveLLMChoice('openai')} className={`bg-black rounded-md flex flex-row hover:border-rose-500 items-center cursor-pointer justify-center py-1 px-2 space-x-1 border-2 ${llm==='openai'&&'border-rose-500'}`}>
                <img src='./openai.png' className='contain h-[30px] invert' />
                <p className='text-center text-xs text-gray-100 whitespace-nowrap'>Open AI</p>
            </div>
            <div onClick={() => saveLLMChoice('claudeai')} className={`${llm==='claudeai'&&'border-rose-500'} hover:border-rose-500 bg-orange-100 rounded-md flex flex-row items-center cursor-pointer justify-center py-1 px-2 space-x-1 border`}>
                <img src='./claude.png' className='contain h-[30px]' />
                <p className='text-center text-xs text-black whitespace-nowrap'>Claude AI</p>
            </div>
        </div>
      </div>
      <div className='w-1/2 h-full flex flex-col items-center'>
        <div className='w-full'>
            <div className='w-full bg-gray-100 text-left rounded-md'>
                <p className='w-full text-left text-sm text-black px-2 py-1'>Organisational Information</p>
            </div>
            <div className='w-full border h-[200px] my-2'>
                <textarea
                    className='w-full h-full text-left bg-black rounded-md px-2 py-2 text-sm text-white'
                    placeholder='Separated by new line'
                    value={orgE}
                    onChange={(e) => setorgE(e.target.value)}
                ></textarea>
            </div>
        </div>
        {
            custE?.map((item, index) => (
                <CustomItem
                    index={index}
                    onSave={(item) => {
                        addcusEntity(item)
                    }}
                    _label={item?.label||''}
                    _terms={item?.terms?.join(',')||''}
                />
            ))
        }
        {
            (custE.length === 0||showNew) && (<CustomItem
                    index={custE.length}
                    onSave={(item) => {
                        addcusEntity(item)
                        setSN(false)
                        getCustomEntties()
                    }}
                />)
        }
        {!showNew&&(<p className='w-full text-sm py-2 text-rose-600 text-left cursor-pointer' onClick={() => setSN(true)}>Add New Custom Entity</p>)}
      </div>
    </div>
  )
}

export default Settings
