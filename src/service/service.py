from __future__ import annotations

import asyncio
import json
import random
import traceback

from tornado.escape import json_decode
from tornado.web import Application, HTTPError, RequestHandler

from datamodels.models import ServiceInput, ServiceOutputAB
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import (
    DailyCostPredictor,
    DailyCostPredictorLinearByDuration,
    DailyCostPredictorML,
    DailyCostPredictorSimple,
)
from solution.find_solution import find_solution


async def run_async_service(port: int):
    app = Application(
        [
            (r"/simple", SimpleSolutionHandler),
            (r"/linear", LinearByDurationSolutionHandler),
            (r"/ml", MainSolutionHandler),
            (r"/ab", ABSolutionHandler),
        ]
    )
    app.listen(port)
    await asyncio.Event().wait()


def run_service(port: int):
    asyncio.run(run_async_service(port))


class SolutionHandler(RequestHandler):
    avg_delay_predictor: AvgDelayPredictor
    daily_cost_predictor: DailyCostPredictor

    def post(self):
        try:
            service_input = json_decode(self.request.body)
            solution = find_solution(
                service_input, self.avg_delay_predictor, self.daily_cost_predictor
            )
            self.write(json.dumps(solution))
        except HTTPError:
            raise
        except Exception:
            traceback.print_exc()
            raise HTTPError(500)


class SimpleSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorSimple()


class LinearByDurationSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorLinearByDuration()


class MainSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorML()


class ABSolutionHandler(RequestHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor_simple = DailyCostPredictorSimple()
    daily_cost_predictor_linear = DailyCostPredictorLinearByDuration()
    daily_cost_predictor_ml = DailyCostPredictorML()

    def post(self):
        try:
            a: str = self.request.headers.get("a-method")  # type: ignore
            b: str = self.request.headers.get("b-method")  # type: ignore
            if a not in {"simple", "linear", "ml"} or b not in {
                "simple",
                "linear",
                "ml",
            }:
                raise HTTPError(404)
            service_input: ServiceInput = json_decode(self.request.body)
            tracks_size = len(service_input["tracks"])
            tracks_half_at_random = set(
                random.sample(
                    [x["id"] for x in service_input["tracks"]], int(tracks_size / 2)
                )
            )
            input_a: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            input_b: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] not in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            solution_a = find_solution(
                input_a,
                self.avg_delay_predictor,
                {
                    "simple": self.daily_cost_predictor_simple,
                    "linear": self.daily_cost_predictor_linear,
                    "ml": self.daily_cost_predictor_ml,
                }[a],
            )
            solution_b = find_solution(
                input_b,
                self.avg_delay_predictor,
                {
                    "simple": self.daily_cost_predictor_simple,
                    "linear": self.daily_cost_predictor_linear,
                    "ml": self.daily_cost_predictor_ml,
                }[b],
            )
            solution: ServiceOutputAB = {"a": solution_a, "b": solution_b}
            self.write(json.dumps(solution))
        except HTTPError:
            raise
        except Exception:
            traceback.print_exc()
            raise HTTPError(500)
