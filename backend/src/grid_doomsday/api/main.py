from __future__ import annotations
from itertools import islice
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from grid_doomsday.cascade import run_cascade
from grid_doomsday.grid_loader import load_case
from grid_doomsday.resource.crossover import estimate
from grid_doomsday.search import exhaustive

app=FastAPI(title='Grid Doomsday Finder API', version='0.1.0')
class SearchRequest(BaseModel):
    case:str='toy'; k:int=Field(2,ge=1,le=6); max_candidates:int=Field(1000,ge=1,le=100000); trip_multiplier:float=Field(1.0,ge=0.0)
class CascadeRequest(BaseModel): case:str='toy'; outages:list[int]=Field(default_factory=list); trip_multiplier:float=1.0

def grid_for(name):
    try:return load_case(name)
    except ValueError as exc: raise HTTPException(400,str(exc))
@app.get('/health')
def health(): return {'status':'ok','evidence':'IMPLEMENTED'}
@app.get('/grids/{case}')
def metadata(case:str):
    grid=grid_for(case); return {'case':case,'buses':len(grid.buses),'branches':len(grid.branches),'load_total':grid.load_total,'metadata':grid.metadata}
@app.post('/cascade')
def cascade(request:CascadeRequest): return run_cascade(grid_for(request.case),tuple(sorted(request.outages)),trip_multiplier=request.trip_multiplier).to_dict()
@app.post('/search')
def search(request:SearchRequest):
    grid=grid_for(request.case); oracle=lambda outage:run_cascade(grid,outage,trip_multiplier=request.trip_multiplier)
    candidates=islice(__import__('grid_doomsday.contingency',fromlist=['enumerate_outages']).enumerate_outages(grid.candidate_branch_ids,request.k),request.max_candidates)
    results=[oracle(outage) for outage in candidates]; best=max(results,key=lambda r:r.s,default=None)
    return {'evidence':'EMULATED','evaluations':len(results),'best':best.to_dict() if best else None,'ranking':[r.to_dict() for r in sorted(results,key=lambda r:r.s,reverse=True)[:10]]}
@app.get('/resource/crossover')
def crossover(candidates:int=1000,oracle_cost:float=1.0): return {'evidence':'ESTIMATED',**estimate(candidates,oracle_cost).__dict__}
