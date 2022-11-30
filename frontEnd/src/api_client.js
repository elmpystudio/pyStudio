import axios from 'axios';
import router from '@/router';

export const API_URL='http://localhost:8000';

axios.interceptors.response.use(function (response) {
    return response
}, function (error) {
    if (error.response.status === 401) {
        localStorage.removeItem('token');
        router.push('/login')
    }
    return Promise.reject(error)
});

//@TODO use single instance for api calls

export const login = ({ username, password }) => axios.post(`${API_URL}/api/token/`, { username, password });

export const register = ({ username, email, password, about, image }) => {
    //axios.post(`${API_URL}/api/register/`, { username, email, password, about, avatar });

    var formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("about", about);

    if(image !== null)
        formData.append("avatar", image);
    
    return axios({
        method: 'post',
        url: `${API_URL}/api/register/`,
        data: formData,
    });
};

export const getProjects = () => axios.get(`${API_URL}/api/accounts/projects/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDashboardItems = (type) => axios.get(`${API_URL}/api/items/dashboard/${type}/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getTableauToken = (ip) => axios.post(`${API_URL}/api/tableau/trusted/`, { ip: ip.replace(/\n/g, '') }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getWorkbooks = () => axios.get(`${API_URL}/api/tableau/workbooks/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const uploadItem = (fileName, file) => {
    const bodyFormData = new FormData();
    bodyFormData.set(fileName, file);
    return axios.post(`${API_URL}/api/items/file_upload/${fileName}/`, bodyFormData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
};

export const uploadDataset = (name, id) => axios.post(`${API_URL}/api/items/datasets/`, { name, file: id }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDatasetById = (id) => axios.get(`${API_URL}/api/items/datasets/?id=${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const createVA = (payload) => axios.post(`${API_URL}/api/items/va/`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getMarketplaceOfferings = () => axios.get(`${API_URL}/api/marketplace/offering/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getMarketplaceOfferingById = (id) => axios.get(`${API_URL}/api/marketplace/offering/?id=${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getMyIP = () => axios.get('http://icanhazip.com/');

export const getItemsSample = (id) => axios.get(`${API_URL}/api/items/sample/${id}/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const purchaseOffering = (data) => axios.post(`${API_URL}/api/marketplace/purchase/`, { ...data }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getHTMLRaport = (id) => axios.get(`${API_URL}/api/items/raport/html/${id}/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const publishOffering = (data) => axios.post(`${API_URL}/api/marketplace/offering/`, { ...data }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const editDataset = (id, payload) => axios.patch(`${API_URL}/api/items/datasets/${id}`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const hubLogin = () => axios.get(`${API_URL}/hub/login/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getSession = () => axios.get(`${API_URL}/api/ses/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    },
});

export const getUser = () => axios.get(`${API_URL}/api/accounts/users/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    },
});

export const updateUser = (payload) => axios.put(`${API_URL}/api/accounts/users/`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getUser_fake = () => axios.get('json/user_fakedata.json', {
});

// services
export const get_services = () => axios.get(`${API_URL}/api/services/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const delete_service = (id) => axios.delete(`${API_URL}/api/services/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const save_services = (payload) => axios.post(`${API_URL}/api/services`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const post_service = (payload) => axios.post(`${API_URL}/api/services/run`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});