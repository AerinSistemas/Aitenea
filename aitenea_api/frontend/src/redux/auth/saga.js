import { all, call, fork, put, takeEvery, select } from 'redux-saga/effects';
import axios from 'axios';
import {
  LOGIN_USER,
  LOAD_USER,
  REGISTER_USER,
  LOGOUT_USER,
  FORGOT_PASSWORD,
  RESET_PASSWORD,
} from '../actions';

import {
  loginUserSuccess,
  loginUserError,
  loadUserSuccess,
  loadUserError,
  registerUserSuccess,
  registerUserError,
  forgotPasswordSuccess,
  forgotPasswordError,
  resetPasswordSuccess,
  resetPasswordError,
} from './actions';

import { adminRoot, loginRoot } from '../../constants/defaultValues';
import { setCurrentUser, setAuthToken, getTokenConfig } from '../../helpers/Utils';
import { getToken } from './selectors';

export function* watchLoginUser() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(LOGIN_USER, loginWithUsernamePassword);
}

const loginWithUsernamePasswordAsync = async (username, password) =>
  // eslint-disable-next-line no-return-await
  axios
    .post(
      '/api/auth/login/', 
      { 
        'username': username, 
        'password': password
      },
      {
        'headers': {
          'Content.Type': 'application/json'
        }
      }
    )
    .then((user) => user)
    .catch((error) => error);

function* loginWithUsernamePassword({ payload }) {
  const { username, password } = payload.user;
  const { history } = payload;
  try {
    const loginUser = yield call(loginWithUsernamePasswordAsync, username, password);
    if (!loginUser.message) {
      setCurrentUser(loginUser.data.user);
      setAuthToken(loginUser.data.token);
      yield put(loginUserSuccess(loginUser.data));
      history.push(adminRoot);
    }
    else {
      const message = 'Check your credentials.';
      yield put(loginUserError(message));
    }
  } catch (error) {
    yield put(loginUserError(error));
  }
}

export function* watchLoadUser() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(LOAD_USER, loadUser);
}

const loadUserAsync = async (token) =>
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/auth/user/', getTokenConfig(token)
    )
    .then((user) => user)
    .catch((error) => error);

function* loadUser({ payload }) {
  const { history } = payload;
  try {
    const token = yield select(getToken);
    const loginUser = yield call(loadUserAsync, token);
    if (!loginUser.message) {
      yield put(loadUserSuccess(loginUser.data));
    }
    else {
      const message = 'Expired session token.';
      yield put(loadUserError(message));
      history.push(loginRoot);
    }
  } catch (error) {
    yield put(loadUserError(error));
    history.push(loginRoot);
  }
}

export function* watchRegisterUser() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(REGISTER_USER, registerWithEmailPassword);
}

const registerWithEmailPasswordAsync = async (email, password) => {
  // eslint-disable-next-line no-return-await
  /*
  await auth
    .createUserWithEmailAndPassword(email, password)
    .then((user) => user)
    .catch((error) => error);
  */
}

function* registerWithEmailPassword({ payload }) {
  const { email, password } = payload.user;
  const { history } = payload;
  try {
    const registerUser = yield call(
      registerWithEmailPasswordAsync,
      email,
      password
    );
    if (!registerUser.message) {
      const item = { uid: registerUser.user.uid, ...currentUser };
      setCurrentUser(item);
      yield put(registerUserSuccess(item));
      history.push(adminRoot);
    } else {
      yield put(registerUserError(registerUser.message));
    }
  } catch (error) {
    yield put(registerUserError(error));
  }
}

export function* watchLogoutUser() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(LOGOUT_USER, logout);
}

const logoutAsync = async (history) => {
  history.push(adminRoot);
};

function* logout({ payload }) {
  const { history } = payload;
  yield call(logoutAsync, history);
}

export function* watchForgotPassword() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(FORGOT_PASSWORD, forgotPassword);
}

const forgotPasswordAsync = async (email) => {
  // eslint-disable-next-line no-return-await
  /*
  return await auth
    .sendPasswordResetEmail(email)
    .then((user) => user)
    .catch((error) => error);
  */
};

function* forgotPassword({ payload }) {
  const { email } = payload.forgotUserMail;
  try {
    const forgotPasswordStatus = yield call(forgotPasswordAsync, email);
    if (!forgotPasswordStatus) {
      yield put(forgotPasswordSuccess('success'));
    } else {
      yield put(forgotPasswordError(forgotPasswordStatus.message));
    }
  } catch (error) {
    yield put(forgotPasswordError(error));
  }
}

export function* watchResetPassword() {
  // eslint-disable-next-line no-use-before-define
  yield takeEvery(RESET_PASSWORD, resetPassword);
}

const resetPasswordAsync = async (resetPasswordCode, newPassword) => {
  // eslint-disable-next-line no-return-await
  /*
  return await auth
    .confirmPasswordReset(resetPasswordCode, newPassword)
    .then((user) => user)
    .catch((error) => error);
  */
};

function* resetPassword({ payload }) {
  const { newPassword, resetPasswordCode } = payload;
  try {
    const resetPasswordStatus = yield call(
      resetPasswordAsync,
      resetPasswordCode,
      newPassword
    );
    if (!resetPasswordStatus) {
      yield put(resetPasswordSuccess('success'));
    } else {
      yield put(resetPasswordError(resetPasswordStatus.message));
    }
  } catch (error) {
    yield put(resetPasswordError(error));
  }
}

export default function* rootSaga() {
  yield all([
    fork(watchLoginUser),
    fork(watchLogoutUser),
    fork(watchLoadUser),
    fork(watchRegisterUser),
    fork(watchForgotPassword),
    fork(watchResetPassword),
  ]);
}
