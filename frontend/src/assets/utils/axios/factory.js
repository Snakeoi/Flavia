import axios from 'axios';

const ApiConnector = axios.create({
    baseURL: '/api',
});

ApiConnector.interceptors.request.use(config => {
  const token = localStorage.getItem('access-token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config;
}, error => {
  return Promise.reject(error);
});

ApiConnector.interceptors.response.use(
    response => {
        console.log(response.status)
        return response
    },
    error => {
        if (error.code === 'ERR_NETWORK') {
            console.log('Connection lost');
        }
        else if (error.response && error.response.status === 401) {
            console.log('Unauthorised');
            // router.push('/login')
        }
        else if (error.response && error.response.status === 403) {
            console.log('Forbidden');
        }
        else if (error.response && error.response.status === 500) {
            console.log('Server Error');
        } else {
            console.log(error.message);
        }
        return Promise.reject(error);
    }
);

export default ApiConnector;