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

const INIT_STATE = {
  allAlgorithmItems: null,
  algorithmItems: null,
  currentAlgorithm: null,
  error: '',
  filter: null,
  searchKeyword: '',
  orderDirection: 'desc',
  orderColumn: null,
  loading: false,
  orderColumns: [
    { column: 'name', label: 'Algorithm name' },
    { column: 'type', label: 'Algorithm type' },
  ],
  selectedItems: [],
  reload: false
};

export default (state = INIT_STATE, action) => {
  switch (action.type) {
    case ALGORITHM_GET_LIST:
      return { ...state, loading: false };

    case ALGORITHM_GET_LIST_SUCCESS:
      return {
        ...state,
        loading: true,
        allAlgorithmItems: action.payload,
        algorithmItems: action.payload,
      };

    case ALGORITHM_GET_LIST_ERROR:
      return { ...state, loading: true, error: action.payload };

    case ALGORITHM_GET_LIST_WITH_FILTER:
      if (action.payload.column === '' || action.payload.value === '') {
        return {
          ...state,
          loading: true,
          algorithmItems: state.allAlgorithmItems,
          filter: null,
        };
      }
      // eslint-disable-next-line no-case-declarations
      const filteredItems = state.allAlgorithmItems.filter(
        (item) => item[action.payload.column] === action.payload.value
      );
      return {
        ...state,
        loading: true,
        algorithmItems: filteredItems,
        filter: {
          column: action.payload.column,
          value: action.payload.value,
        },
      };

    case ALGORITHM_CHANGE_LIST_ORDER:
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

    case ALGORITHM_GET_LIST_WITH_ORDER:
      if (action.payload === '') {
        return {
          ...state,
          loading: true,
          algorithmItems: state.algorithmItems,
          orderColumn: null,
        };
      }
      // eslint-disable-next-line no-case-declarations
      const sortedItems = state.algorithmItems.sort((a, b) => {
        if (a[action.payload] < b[action.payload]) return -1;
        if (a[action.payload] > b[action.payload]) return 1;
        return 0;
      });
      return {
        ...state,
        loading: true,
        algorithmItems: sortedItems,
        orderColumn: state.orderColumns.find(
          (x) => x.column === action.payload
        ),
      };

    case ALGORITHM_GET_LIST_SEARCH:
      if (action.payload === '') {
        return { ...state, algorithmItems: state.allAlgorithmItems };
      }
      // eslint-disable-next-line no-case-declarations
      const keyword = action.payload.toLowerCase();
      // eslint-disable-next-line no-case-declarations
      let searchItems = state.allAlgorithmItems.filter(
        (item) =>
          item.class_name.toLowerCase().indexOf(keyword) > -1 ||
          item.type.toLowerCase().indexOf(keyword) > -1
      );
      return {
        ...state,
        loading: true,
        algorithmItems: searchItems,
        searchKeyword: action.payload,
      };

    case ALGORITHM_SELECTED_ITEMS_CHANGE:
      return { ...state, loading: true, selectedItems: action.payload };

    case ALGORITHM_GET_DETAILS:
      return { ...state, loading: false };

    case ALGORITHM_GET_DETAILS_SUCCESS:
      return {
        ...state,
        loading: true,
        currentAlgorithm: action.payload,
      };

    case ALGORITHM_GET_DETAILS_ERROR:
      return { ...state, loading: true, error: action.payload };

    default:
      return { ...state };
  }
};
