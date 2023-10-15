import axios from 'axios';
import router from '@/router';

export const API_URL = 'http://localhost:8000';
export const JUPYTERHUP_URL = 'http://localhost:3000';

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

export const register = ({ username, email, password, about, image }) => {
    //axios.post(`${API_URL}/api/register/`, { username, email, password, about, avatar });

    var formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("about", about);

    if (image !== null)
        formData.append("avatar", image);

    return axios({
        method: 'post',
        url: `${API_URL}/api/users/register/`,
        data: formData,
    });
};

export const login = ({ username, password }) => axios.post(`${API_URL}/api/users/login/`, { username, password });

export const verify = ({ email, otp }) => axios.post(`${API_URL}/api/users/verify/`, { email, otp });

// export const getDashboarddatasets = (type) => axios.get(`${API_URL}/api/datasets/dashboard/${type}/`, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     }
// });

export const getWorkbooks = () => axios.get(`${API_URL}/api/tableau/workbooks/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

// START DATASET
// DATASET[GET, GET<id>, POST], smaple, report
export const createDataset = (payload) => {
    const formdata = new FormData();
    for (var key in payload)
        formdata.append(key, payload[key]);

    return axios.post(`${API_URL}/api/datasets/`, formdata, {
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
};

export const updateDataset = (id, payload) => axios.put(`${API_URL}/api/datasets/${id}`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDatasets = () => axios.get(`${API_URL}/api/datasets/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDataset = (id) => axios.get(`${API_URL}/api/datasets/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const deleteDataset = (id) => axios.delete(`${API_URL}/api/datasets/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDatasetsPublic = () => axios.get(`${API_URL}/api/datasets/public`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDatasetSample = (id) => axios.get(`${API_URL}/api/datasets/sample/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getDatasetRaport = (id) => axios.get(`${API_URL}/api/datasets/raport/html/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});
// END DATASET

// START MARKETPLACE
export const getMarketplaceDatasets = () => axios.get(`${API_URL}/api/marketplace/datasets`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getMarketplaceMlModels = () => axios.get(`${API_URL}/api/marketplace/ml_models`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const downloadDataset = (id) => axios.get(`${API_URL}/api/marketplace/datasets/download/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const downloadMl_model = (id) => axios.get(`${API_URL}/api/marketplace/ml_models/download/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const datasetsAdd = (id, payload) => axios.post(`${API_URL}/api/marketplace/datasets/add/${id}`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const ml_modelsAdd = (id, payload) => axios.post(`${API_URL}/api/marketplace/ml_models/add/${id}`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});
// END MARKETPLACE

// START NOTIFICATION
// export const getNotifications = () => axios.get(`${API_URL}/api/notifications/`, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     }
// });

// export const createNotification = (payload) => axios.post(`${API_URL}/api/notifications/`, payload, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     }
// });

// end NOTIFICATION


// export const denyNotification = (id) => axios.get(`${API_URL}/api/notifications/deny/${id}`, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     }
// });
// end NOTIFICATION

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

export const purchaseOffering = (data) => axios.post(`${API_URL}/api/marketplace/purchase/`, { ...data }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const publishOffering = (data) => axios.post(`${API_URL}/api/marketplace/offering/`, { ...data }, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

// export const hubLogin = () => axios.get(`${API_URL}/hub/login/`, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     }
// });

// export const getSession = () => axios.get(`${API_URL}/api/ses/`, {
//     headers: {
//         Authorization: `Bearer ${localStorage.getItem('token')}`
//     },
// });

// users
export const getUser = () => axios.get(`${API_URL}/api/users/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    },
});

export const updateUser = (payload) => axios.put(`${API_URL}/api/users/`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const getUser_fake = () => axios.get('json/user_fakedata.json', {
});

// ml_models
export const get_mlModels = () => axios.get(`${API_URL}/api/ml_models/`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const delete_mlModel = (id) => axios.delete(`${API_URL}/api/ml_models/${id}`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const run_mlModels1 = (payload) => axios.post(`${API_URL}/api/ml_models/run1`, payload, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const run_mlModels2 = (payload) => {
    const formdata = new FormData();
    for (var key in payload)
        formdata.append(key, payload[key]);

    return axios.post(`${API_URL}/api/ml_models/run2`, formdata, {
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
};

// jupyterhub
export const jupyterhub_open = () => axios.get(`${API_URL}/api/jupyterhub/open`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});

export const jupyterhub_sync = () => axios.get(`${API_URL}/api/jupyterhub/sync`, {
    headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
});
