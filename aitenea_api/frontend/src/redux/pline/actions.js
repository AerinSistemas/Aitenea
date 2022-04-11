// eslint-disable-next-line import/no-cycle
import {
  PLINE_GET_LIST,
  PLINE_GET_LIST_SUCCESS,
  PLINE_GET_LIST_ERROR,
  PLINE_GET_LIST_WITH_FILTER,
  PLINE_CHANGE_LIST_ORDER,
  PLINE_GET_LIST_WITH_ORDER,
  PLINE_GET_LIST_SEARCH,
  PLINE_SELECTED_ITEMS_CHANGE,
  PLINE_DELETE,
  PLINE_DELETE_SUCCESS,
  PLINE_DELETE_ERROR,
  PLINE_GET_DETAILS,
  PLINE_GET_DETAILS_SUCCESS,
  PLINE_GET_DETAILS_ERROR,
  STEP_GET_LIST_BY_PLINE,
  STEP_GET_LIST_BY_PLINE_SUCCESS,
  STEP_GET_LIST_BY_PLINE_ERROR,
} from '../actions';

export const getPlineList = () => ({
  type: PLINE_GET_LIST,
});

export const getPlineListSuccess = (items) => ({
  type: PLINE_GET_LIST_SUCCESS,
  payload: items,
});

export const getPlineListError = (error) => ({
  type: PLINE_GET_LIST_ERROR,
  payload: error,
});

export const getPlineListWithFilter = (column, value) => ({
  type: PLINE_GET_LIST_WITH_FILTER,
  payload: { column, value },
});

export const changePlineListOrder = () => ({
  type: PLINE_CHANGE_LIST_ORDER,
});

export const getPlineListWithOrder = (column) => ({
  type: PLINE_GET_LIST_WITH_ORDER,
  payload: column,
});

export const getPlineListSearch = (keyword) => ({
  type: PLINE_GET_LIST_SEARCH,
  payload: keyword,
});

export const selectedPlineItemsChange = (selectedItems) => ({
  type: PLINE_SELECTED_ITEMS_CHANGE,
  payload: selectedItems,
});

export const deletePline = () => ({
  type: PLINE_DELETE,
});

export const deletePlineSuccess = () => ({
  type: PLINE_DELETE_SUCCESS,
});

export const deletePlineError = (error) => ({
  type: PLINE_DELETE_ERROR,
  payload: error,
});

export const getPlineDetails = () => ({
  type: PLINE_GET_DETAILS,
});

export const getPlineDetailsSuccess = (item) => ({
  type: PLINE_GET_DETAILS_SUCCESS,
  payload: item,
});

export const getPlineDetailsError = (error) => ({
  type: PLINE_GET_DETAILS_ERROR,
  payload: error,
});

export const getStepListByPline = () => ({
  type: STEP_GET_LIST_BY_PLINE,
});

export const getStepListByPlineSuccess = (items) => ({
  type: STEP_GET_LIST_BY_PLINE_SUCCESS,
  payload: items,
});

export const getStepListByPlineError = (error) => ({
  type: STEP_GET_LIST_BY_PLINE_ERROR,
  payload: error,
});