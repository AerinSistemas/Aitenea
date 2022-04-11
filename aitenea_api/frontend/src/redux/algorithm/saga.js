import { all, call, fork, put, takeEvery, select } from 'redux-saga/effects';
import { getTokenConfig } from '../../helpers/Utils';
import axios from 'axios';

import { ALGORITHM_GET_LIST, ALGORITHM_GET_DETAILS } from '../actions';

import {
  getAlgorithmListSuccess,
  getAlgorithmListError,
  getAlgorithmDetailsSuccess,
  getAlgorithmDetailsError,
} from './actions';

import { getToken } from '../auth/selectors';
import { getSelectedItems } from './selectors';

const getAlgorithmListRequest = async (token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/classes/', getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getAlgorithmListItems() {
  try {
    const token = yield select(getToken);
    const response = yield call(getAlgorithmListRequest, token);
    yield put(getAlgorithmListSuccess(response));
  } catch (error) {
    yield put(getAlgorithmListError(error));
  }
}

const getAlgorithmDetailsRequest = async (token, algorithmid) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/classes/${algorithmid}/`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getAlgorithmDetailsItem() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    const response = yield call(getAlgorithmDetailsRequest, token, selectedItems[0]);
    yield put(getAlgorithmDetailsSuccess(response));
  } catch (error) {
    yield put(getAlgorithmDetailsError(error));
  }
}

export function* watchGetList() {
  yield takeEvery(ALGORITHM_GET_LIST, getAlgorithmListItems);
}

export function* watchGetDetails() {
  yield takeEvery(ALGORITHM_GET_DETAILS, getAlgorithmDetailsItem);
}

export default function* rootSaga() {
  yield all([fork(watchGetList)]);
  yield all([fork(watchGetDetails)]);
}
