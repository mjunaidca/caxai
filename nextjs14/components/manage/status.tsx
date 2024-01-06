import clsx from 'clsx';
import { CheckIcon, ClockIcon } from 'lucide-react';

export default function TodoStatus({ status }: { status: boolean }) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-2 py-1 text-xs',
        {
          'bg-gray-100 text-gray-500': status === false,
          'bg-green-500 text-white': status === true,
        },
      )}
    >
      {status === false ? (
        <>
          Pending
          <ClockIcon className="ml-1 w-4 text-gray-500" />
        </>
      ) : null}
      {status === true ? (
        <>
          Done
          <CheckIcon className="ml-1 w-4 text-white" />
        </>
      ) : null}
    </span>
  );
}
