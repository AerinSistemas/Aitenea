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

const INIT_STATE = {
  allPlineItems: null,
  plineItems: null,
  currentPline: null,
  allStepItems: null,
  stepItems: null,
  error: '',
  filter: null,
  searchKeyword: '',
  orderDirection: 'desc',
  orderColumn: null,
  loading: false,
  loadingStep: false,
  orderColumns: [
    { column: 'name', label: 'Pline name' },
    { column: 'creation_timestamp', label: 'Creation date' },
  ],
  selectedItems: [],
  reload: false
};

export default (state = INIT_STATE, action) => {
  switch (action.type) {
    case PLINE_GET_LIST:
      return { ...state, loading: false };

    case PLINE_GET_LIST_SUCCESS:
      return {
        ...state,
        loading: true,
        allPlineItems: action.payload,
        plineItems: action.payload,
      };

    case PLINE_GET_LIST_ERROR:
      return { ...state, loading: true, error: action.payload };

    case PLINE_GET_LIST_WITH_FILTER:
      if (action.payload.column === '' || action.payload.value === '') {
        return {
          ...state,
          loading: true,
          plineItems: state.allPlineItems,
          filter: null,
        };
      }
      // eslint-disable-next-line no-case-declarations
      const filteredItems = state.allPlineItems.filter(
        (item) => item[action.payload.column] === action.payload.value
      );
      return {
        ...state,
        loading: true,
        plineItems: filteredItems,
        filter: {
          column: action.payload.column,
          value: action.payload.value,
        },
      };

    case PLINE_CHANGE_LIST_ORDER:
      if (state.orderDirection === 'asc') {
        return { 
          ...state, 
          loading: true, 
          orderDirection: 'desc' 
        };
      }
      else {
        return { 
          ...state, 
          loading: true, 
          orderDirection: 'asc' 
        };
      }

    case PLINE_GET_LIST_WITH_ORDER:
      if (action.payload === '') {
        return {
          ...state,
          loading: true,
          plineItems: state.plineItems,
          orderColumn: null,
        };
      }
      // eslint-disable-next-line no-case-declarations
      const sortedItems = state.plineItems.sort((a, b) => {
        if (a[action.payload] < b[action.payload]) return -1;
        if (a[action.payload] > b[action.payload]) return 1;
        return 0;
      });
      return {
        ...state,
        loading: true,
        plineItems: sortedItems,
        orderColumn: state.orderColumns.find(
          (x) => x.column === action.payload
        ),
      };

    case PLINE_GET_LIST_SEARCH:
      if (action.payload === '') {
        return { ...state, plineItems: state.allPlineItems };
      }
      // eslint-disable-next-line no-case-declarations
      const keyword = action.payload.toLowerCase();
      // eslint-disable-next-line no-case-declarations
      let searchItems = state.allPlineItems.filter(
        (item) =>
          item.name.toLowerCase().indexOf(keyword) > -1 ||
          item.description.toLowerCase().indexOf(keyword) > -1
      );
      return {
        ...state,
        loading: true,
        plineItems: searchItems,
        searchKeyword: action.payload,
      };

    case PLINE_SELECTED_ITEMS_CHANGE:
      return { ...state, loading: true, selectedItems: action.payload };

    case PLINE_DELETE:
      return { ...state, loading: false, reload: false };

    case PLINE_DELETE_SUCCESS:
      return { ...state, 
        loading: true, 
        reload: true, 
        selectedItems: []
      };

    case PLINE_DELETE_ERROR:
      return { 
        ...state, 
        loading: true, 
        reload: true, 
        selectedItems: [],
        error: action.payload 
      };

    case PLINE_GET_DETAILS:
      return { ...state, loading: false };

    case PLINE_GET_DETAILS_SUCCESS:
      return {
        ...state,
        loading: true,
        currentPline: action.payload,
      };

    case PLINE_GET_DETAILS_ERROR:
      return { ...state, loading: true, error: action.payload };

    case STEP_GET_LIST_BY_PLINE:
      return { ...state, loadingStep: false };

    case STEP_GET_LIST_BY_PLINE_SUCCESS:
      return {
        ...state,
        loadingStep: true,
        allStepItems: action.payload,
        stepItems: action.payload,
      };

    case STEP_GET_LIST_BY_PLINE_ERROR:
      return { ...state, loadingStep: true, error: action.payload };

    default:
      return { ...state };
  }
};
