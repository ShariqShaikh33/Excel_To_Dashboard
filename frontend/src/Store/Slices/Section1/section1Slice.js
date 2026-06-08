import { createSlice } from "@reduxjs/toolkit";

export const section1Slice = createSlice({
    name:"Section1",
    initialState: {},
    reducers:{
        setSection1DataReducer: (state, action) => {
            return{...state,...action.payload,}
        }
    }
})

export const {setSection1DataReducer} = section1Slice.actions;
export default section1Slice.reducer;