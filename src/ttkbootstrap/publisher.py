from typing import Dict, Callable, Any, Set


class Publisher:

    _subscribers: Dict[str, Set[Callable]] = {}

    @staticmethod
    def add(event, callback):
        """Subscribe to an event

        Parameters
        ----------
        event : str
            The event name

        callback : Callable
            A function to call
        """
        if event not in Publisher._subscribers:
            Publisher._subscribers[event] = {callback}
        else:
            Publisher._subscribers[event].add(callback)

    @staticmethod
    def get(event):
        """Get a set of subscribers for this event.

        Parameters
        ----------
        event : str
            An event name.

        Returns
        -------
        set
            A set of callbacks
        """
        return Publisher._subscribers.get(event, set())

    @staticmethod
    def dispatch(event, message=None):
        """Dispatch an event with an optional message passed to the callback.

        Parameters
        ----------
        event : str
            The event name.

        message : Dict[str, Any]
            A message passed to the callback.
        """
        subs = Publisher.get(event)
        for callback in subs:
            if message is None:
                callback()
            else:
                callback(message)
