// eslint-disable-next-line import/no-cycle
import {
  ALGORITHM_GET_LIST,
  ALGORITHM_GET_LIST_SUCCESS,
  ALGORITHM_GET_LIST_ERROR,
  ALGORITHM_GET_LIST_WITH_FILTER,
  ALGORITHM_CHANGE_LIST_ORDER,
  ALGORITHM_GET_LIST_WITH_ORDER,
  ALGORITHM_GET_LIST_SEARCH,
  ALGORITHM_SELECTED_ITEMS_CHANGE,
  ALGORITHM_GET_DETAILS,
  ALGORITHM_GET_DETAILS_SUCCESS,
  ALGORITHM_GET_DETAILS_ERROR,
} from '../actions';

export const getAlgorithmList = () => ({
  type: ALGORITHM_GET_LIST,
});

export const getAlgorithmListSuccess = (items) => ({
  type: ALGORITHM_GET_LIST_SUCCESS,
  payload: items,
});

export const getAlgorithmListError = (error) => ({
  type: ALGORITHM_GET_LIST_ERROR,
  payload: error,
});

export const getAlgorithmListWithFilter = (column, value) => ({
  type: ALGORITHM_GET_LIST_WITH_FILTER,
  payload: { column, value },
});

export const changeAlgorithmListOrder = () => ({
  type: ALGORITHM_CHANGE_LIST_ORDER,
});

export const getAlgorithmListWithOrder = (column) => ({
  type: ALGORITHM_GET_LIST_WITH_ORDER,
  payload: column,
});

export const getAlgorithmListSearch = (keyword) => ({
  type: ALGORITHM_GET_LIST_SEARCH,
  payload: keyword,
});

export const selectedAlgorithmItemsChange = (selectedItems) => ({
  type: ALGORITHM_SELECTED_ITEMS_CHANGE,
  payload: selectedItems,
});

export const getAlgorithmDetails = () => ({
  type: ALGORITHM_GET_DETAILS,
});

export const getAlgorithmDetailsSuccess = (item) => ({
  type: ALGORITHM_GET_DETAILS_SUCCESS,
  payload: item,
});

export const getAlgorithmDetailsError = (error) => ({
  type: ALGORITHM_GET_DETAILS_ERROR,
  payload: error,
});
