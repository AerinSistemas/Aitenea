import {
  LOGIN_USER,
  LOGIN_USER_SUCCESS,
  LOGIN_USER_ERROR,
  LOAD_USER,
  LOAD_USER_SUCCESS,
  LOAD_USER_ERROR,
  REGISTER_USER,
  REGISTER_USER_SUCCESS,
  REGISTER_USER_ERROR,
  LOGOUT_USER,
  FORGOT_PASSWORD,
  FORGOT_PASSWORD_SUCCESS,
  FORGOT_PASSWORD_ERROR,
  RESET_PASSWORD,
  RESET_PASSWORD_SUCCESS,
  RESET_PASSWORD_ERROR,
} from '../actions';
import { getCurrentUser, getAuthToken, setAuthToken, setCurrentUser } from '../../helpers/Utils';

const INIT_STATE = {
  currentUser: getCurrentUser(),
  token: getAuthToken(),
  forgotUserMail: '',
  newPassword: '',
  resetPasswordCode: '',
  loading: false,
  error: '',
};

export default (state = INIT_STATE, action) => {
  switch (action.type) {
    case LOGIN_USER:
    case LOAD_USER:
      return { ...state, loading: true, error: '' };
    case LOGIN_USER_SUCCESS:
      setAuthToken(action.payload.token);
      return {
        ...state,
        loading: false,
        currentUser: action.payload.user,
        token: action.payload.token,
        error: '',
      };
    case LOGIN_USER_ERROR:
      setCurrentUser();
      setAuthToken();
      return {
        ...state,
        loading: false,
        currentUser: null,
        token: null,
        error: action.payload.message,
      };
    case LOAD_USER_SUCCESS:
      return { 
        ...state, 
        loading: false, 
        currentUser: action.payload.user, 
        error: '' 
      };
    case FORGOT_PASSWORD:
      return { ...state, loading: true, error: '' };
    case FORGOT_PASSWORD_SUCCESS:
      return {
        ...state,
        loading: false,
        forgotUserMail: action.payload,
        error: '',
      };
    case FORGOT_PASSWORD_ERROR:
      return {
        ...state,
        loading: false,
        forgotUserMail: '',
        error: action.payload.message,
      };
    case RESET_PASSWORD:
      return { ...state, loading: true, error: '' };
    case RESET_PASSWORD_SUCCESS:
      return {
        ...state,
        loading: false,
        newPassword: action.payload,
        resetPasswordCode: '',
        error: '',
      };
    case RESET_PASSWORD_ERROR:
      return {
        ...state,
        loading: false,
        newPassword: '',
        resetPasswordCode: '',
        error: action.payload.message,
      };
    case REGISTER_USER:
      return { ...state, loading: true, error: '' };
    case REGISTER_USER_SUCCESS:
      return {
        ...state,
        loading: false,
        currentUser: action.payload,
        error: '',
      };
    case REGISTER_USER_ERROR:
      return {
        ...state,
        loading: false,
        currentUser: null,
        error: action.payload.message,
      };
    case LOGOUT_USER:
    case LOAD_USER_ERROR:
      setCurrentUser();
      setAuthToken();
      return { 
        ...state, 
        loading: false, 
        currentUser: null, 
        token: null, 
        error: '' 
      };
      
    default:
      return { ...state };
  }
};
