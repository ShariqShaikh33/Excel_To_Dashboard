import { createSlice } from "@reduxjs/toolkit";

export const section3Slice = createSlice({
    name:"Section3",
    initialState: {},
    reducers:{
        setSection3DataReducer:(state,action)=>{
            return{...state,...action.payload};
        }
    }
})

export const {setSection3DataReducer} = section3Slice.actions;
export default section3Slice.reducer;